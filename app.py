from flask import Flask
from routes.summarize import summarize_bp
from routes.quiz import quiz_bp
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
# Register routes
app.register_blueprint(summarize_bp)
app.register_blueprint(quiz_bp)

if __name__ == '__main__':
    app.run(debug=True)
