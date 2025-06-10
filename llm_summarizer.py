from flask import Flask, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
import os

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = ""


@app.route('/summarize', methods=['POST'])
def summarize_url():
    data = request.json

    if 'url' not in data:
        return jsonify({'error': ' URL is required'}), 400
    
    url = data['url']
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()

        llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0)

        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run(docs)

        return jsonify({'summary': summary})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


