from flask import Blueprint, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain.chains import LLMChain
import json
import os


quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.json

    if 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    url = data['url']

    try:
        loader = WebBaseLoader(url)
        docs = loader.load()

        prompt = PromptTemplate(
            input_variables=["content"],
            template="""
                Read the following content and generate 10 multiple-choice quiz questions. 
                Each question must have 4 options (A, B, C, D) and include the correct answer.

                Content:
                {content}

                Output the quiz in JSON format:
                [
                {{
                    "question": "...",
                    "options": {{
                    "A": "...",
                    "B": "...",
                    "C": "...",
                    "D": "..."
                    }},
                    "answer": "C"
                }},
                ...
                ]
            """
        )

        llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash-latest", 
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        chain = LLMChain(llm=llm, prompt=prompt)

        full_content = "\n".join([doc.page_content for doc in docs])
        quiz_output = chain.run({"content": full_content})

        try:
            quiz_data = json.loads(quiz_output)
        except:
            quiz_data = {"raw_output": quiz_output}

        return jsonify(quiz_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
