## Integrate our code Groq API with Flask
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from flask import Flask, render_template, request

# Load environment variables from .env file
load_dotenv()

# Get Groq API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Prompt Templates
first_input_prompt = PromptTemplate(
    input_variables=['name'],
    template="Tell me about celebrity {name}"
)

second_input_prompt = PromptTemplate(
    input_variables=['person'],
    template="when was {person} born"
)

third_input_prompt = PromptTemplate(
    input_variables=['dob'],
    template="Mention 5 major events happened around {dob} in the world"
)

## Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.8,
    api_key=groq_api_key
)

# Store results in session
results_store = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    person_info = None
    dob_info = None
    events_info = None
    
    if request.method == 'POST':
        input_text = request.form.get('search')
        
        if input_text:
            try:
                # First chain - Get person info
                formatted_prompt_1 = first_input_prompt.format(name=input_text)
                person_response = llm.invoke(formatted_prompt_1)
                person_info = person_response.content
                
                # Second chain - Get DOB
                formatted_prompt_2 = second_input_prompt.format(person=person_info)
                dob_response = llm.invoke(formatted_prompt_2)
                dob_info = dob_response.content
                
                # Third chain - Get major events
                formatted_prompt_3 = third_input_prompt.format(dob=dob_info)
                events_response = llm.invoke(formatted_prompt_3)
                events_info = events_response.content
                
                result = {
                    'person': person_info,
                    'dob': dob_info,
                    'description': events_info
                }
            except Exception as e:
                result = {'error': str(e)}
    
    return render_template('index.html', result=result, person_info=person_info, dob_info=dob_info, events_info=events_info)


if __name__ == '__main__':
    app.run(debug=True)


# if __name__ == '__main__':
#     app.run(debug=True)