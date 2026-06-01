from flask import Flask, request, jsonify, render_template_string
from ingest import ingest_pdf
from rag import ask, get_collections
import os

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>PDF RAG Chat</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
    h1 { font-size: 22px; margin-bottom: 24px; }
    .card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
    .card h2 { font-size: 15px; margin-bottom: 12px; color: #555; }
    input[type=file], select { width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 6px; }
    input[type=text] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
    button { padding: 9px 20px; background: #1a1a1a; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; }
    button:hover { background: #333; }
    #chat { min-height: 200px; max-height: 400px; overflow-y: auto; margin-bottom: 12px; }
    .msg { padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
    .msg .who { font-size: 12px; font-weight: 600; color: #888; margin-bottom: 4px; }
    .msg .txt { font-size: 14px; line-height: 1.6; }
    .sources { margin-top: 8px; font-size: 12px; color: #888; background: #f9f9f9; padding: 8px; border-radius: 4px; }
    .status { font-size: 13px; color: #555; margin-top: 8px; }
    .row { display: flex; gap: 8px; }
    .row input { flex: 1; }
  </style>
</head>
<body>
  <h1>📄 PDF RAG Chat</h1>

  <div class="card">
    <h2>1. Upload a PDF</h2>
    <input type="file" id="pdf-file" accept=".pdf">
    <button onclick="uploadPDF()">Upload & Process</button>
    <div class="status" id="upload-status"></div>
  </div>

  <div class="card">
    <h2>2. Select document & ask a question</h2>
    <select id="doc-select"><option>— upload a PDF first —</option></select>
    <div id="chat"></div>
    <div class="row">
      <input type="text" id="question" placeholder="Ask anything about the document..." onkeydown="if(event.key==='Enter')ask()">
      <button onclick="ask()">Ask</button>
    </div>
  </div>

  <script>
    async function uploadPDF() {
      const file = document.getElementById('pdf-file').files[0];
      if (!file) return alert('Select a PDF first');
      const status = document.getElementById('upload-status');
      status.textContent = 'Processing... (this may take 30-60 seconds)';
      const fd = new FormData();
      fd.append('file', file);
      const res = await fetch('/upload', { method: 'POST', body: fd });
      const data = await res.json();
      if (data.error) { status.textContent = 'Error: ' + data.error; return; }
      status.textContent = `Done! ${data.chunks} chunks indexed from ${data.filename}`;
      loadDocs();
    }

    async function loadDocs() {
      const res = await fetch('/collections');
      const data = await res.json();
      const sel = document.getElementById('doc-select');
      sel.innerHTML = data.collections.map(c => `<option value="${c}">${c}</option>`).join('');
    }

    async function ask() {
      const q = document.getElementById('question').value.trim();
      const col = document.getElementById('doc-select').value;
      if (!q || col.startsWith('—')) return;
      document.getElementById('question').value = '';
      addMsg('You', q, null);
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q, collection: col })
      });
      const data = await res.json();
      addMsg('AI', data.answer, data.chunks);
    }

    function addMsg(who, text, chunks) {
      const chat = document.getElementById('chat');
      const div = document.createElement('div');
      div.className = 'msg';
      let src = '';
      if (chunks) src = `<div class="sources">📎 Based on ${chunks.length} chunks from the document</div>`;
      div.innerHTML = `<div class="who">${who}</div><div class="txt">${text}</div>${src}`;
      chat.appendChild(div);
      chat.scrollTop = chat.scrollHeight;
    }

    loadDocs();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "no file"})
    path = os.path.join("uploads", file.filename)
    file.save(path)
    collection_name, chunks = ingest_pdf(path)
    return jsonify({"filename": file.filename, "chunks": chunks, "collection": collection_name})

@app.route("/collections")
def collections():
    return jsonify({"collections": get_collections()})

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.json
    result = ask(data["question"], data["collection"])
    return jsonify(result)

if __name__ == "__main__":
    print("🚀 RAG app running at http://localhost:5000")
    app.run(port=5000, debug=True)