from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from utils.summarize import generate_summary
from utils.sentiment import analyze_sentiment
from utils.export import export_pdf, export_txt
from utils.tts import generate_audio
from models.note_model import db, Note
from utils.extract import extract_text_from_file
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-dev-key')  # Fallback for local dev

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database', 'notes.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        manual_text = request.form.get('text', '')
        summary_length = request.form.get('length', 'medium')
        file = request.files.get('file')

        text = manual_text.strip()
        if file and not text:
            text = extract_text_from_file(file)

        if not text.strip():
            session['error'] = "No input text found!"
            session['text'] = ''
            return redirect(url_for('index'))

        summary = generate_summary(text, length=summary_length)
        sentiment = analyze_sentiment(text)

        new_note = Note(content=text, summary=summary, sentiment=sentiment)
        db.session.add(new_note)
        db.session.commit()

        session['summary'] = summary
        session['sentiment'] = sentiment
        session['text'] = text
        session['error'] = None

        return redirect(url_for('index'))

    # Handle GET and display session values
    summary = session.pop('summary', None)
    sentiment = session.pop('sentiment', None)
    text = session.pop('text', '')
    error = session.pop('error', None)

    return render_template("index.html", summary=summary, sentiment=sentiment, text=text, error=error)


@app.route('/export/pdf', methods=['POST'])
def export_as_pdf():
    text = request.form.get('text', '')
    pdf_path = export_pdf(text)
    return send_file(pdf_path, as_attachment=True)


@app.route('/export/txt', methods=['POST'])
def export_as_txt():
    text = request.form.get('text', '')
    txt_path = export_txt(text)
    return send_file(txt_path, as_attachment=True)


@app.route('/voice', methods=['POST'])
def voice_summary():
    summary = request.form['summary']
    audio_path, filename = generate_audio(summary)
    return jsonify({'audio_url': f'/static/audio/{filename}'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080)