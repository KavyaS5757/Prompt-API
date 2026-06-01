from flask import Flask, render_template_string, request, jsonify
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Get Groq API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Function to get response from Groq LLM
def getBlogResponse(input_text, no_words, blog_style):
    try:
        # Initialize Groq LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.01,
            api_key=groq_api_key
        )
        
        # Prompt Template
        template = """
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
        """
        
        prompt = PromptTemplate(
            input_variables=["blog_style", "input_text", "no_words"],
            template=template
        )
        
        # Generate response from Groq LLM
        response = llm.invoke(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

# HTML Template for the web interface
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Generate Blogs</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
        }
        h1 { 
            color: #333;
            margin-bottom: 30px;
            text-align: center;
            font-size: 32px;
        }
        .form-group { 
            margin-bottom: 20px; 
        }
        label { 
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
            font-size: 14px;
        }
        input[type="text"], 
        select { 
            width: 100%; 
            padding: 12px; 
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        button { 
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 20px;
        }
        button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        #output { 
            margin-top: 30px; 
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            border-radius: 6px;
            line-height: 1.8;
            color: #333;
            display: none;
            max-height: 500px;
            overflow-y: auto;
        }
        #output.show { 
            display: block; 
        }
        .loading { 
            display: none;
            text-align: center;
            color: #667eea;
            font-weight: 600;
            padding: 20px;
        }
        .loading.show { 
            display: block; 
        }
        .error {
            color: #d32f2f;
            padding: 15px;
            background: #ffebee;
            border-radius: 6px;
            margin-top: 10px;
            display: none;
        }
        .error.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Generate Blogs</h1>
        
        <form id="blogForm" onsubmit="generateBlog(event)">
            <div class="form-group">
                <label for="topic">Blog Topic *</label>
                <input type="text" id="topic" placeholder="Enter the blog topic..." required>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="words">Number of Words *</label>
                    <input type="text" id="words" placeholder="e.g., 500" required>
                </div>
                
                <div class="form-group">
                    <label for="style">Writing Style *</label>
                    <select id="style" required>
                        <option value="Researchers">Researchers</option>
                        <option value="Data Scientist">Data Scientist</option>
                        <option value="Common People">Common People</option>
                    </select>
                </div>
            </div>
            
            <button type="submit" id="generateBtn">Generate Blog</button>
        </form>
        
        <div class="loading" id="loading">
            <div>⏳ Generating your blog... Please wait...</div>
        </div>
        
        <div class="error" id="error"></div>
        <div id="output"></div>
    </div>

    <script>
        async function generateBlog(event) {
            event.preventDefault();
            
            const topic = document.getElementById('topic').value.trim();
            const words = document.getElementById('words').value.trim();
            const style = document.getElementById('style').value;
            const output = document.getElementById('output');
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const generateBtn = document.getElementById('generateBtn');
            
            // Clear previous output
            output.classList.remove('show');
            error.classList.remove('show');
            
            // Show loading
            loading.classList.add('show');
            generateBtn.disabled = true;
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        topic: topic,
                        words: words,
                        style: style
                    })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    error.textContent = 'Error: ' + data.error;
                    error.classList.add('show');
                } else {
                    output.innerHTML = data.blog;
                    output.classList.add('show');
                }
            } catch (err) {
                error.textContent = 'Error: ' + err.message;
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
                generateBtn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        topic = data.get("topic", "").strip()
        words = data.get("words", "").strip()
        style = data.get("style", "").strip()
        
        if not topic or not words or not style:
            return jsonify({"error": "All fields are required"}), 400
        
        blog = getBlogResponse(topic, words, style)
        
        # Format the blog with line breaks
        formatted_blog = blog.replace("\n", "<br>")
        
        return jsonify({"blog": formatted_blog})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    print("🚀 Blog Generation app running at http://localhost:5000")
    app.run(port=5000, debug=True)