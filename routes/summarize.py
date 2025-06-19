from flask import  Blueprint, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
import os

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/summarize', methods=['POST'])
def summarize_url():
    data = request.json

    if 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()

        llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash-latest", 
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run(docs)

        return jsonify({'summary': summary})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


