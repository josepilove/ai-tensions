from dotenv import load_dotenv
load_dotenv()  # This should be at the very beginning to load environment variables

from flask import Flask, render_template
from config.config import SECRET_KEY
from routes.main import main
from routes.report import report

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(report)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)