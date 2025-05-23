from flask import Flask, render_template, request
import spacy
import os

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = ""
    if request.method == 'POST':
        note = request.form['note']
        doc = nlp(note)
        analysis = [(ent.text, ent.label_) for ent in doc.ents]
    return render_template('index.html', analysis=analysis)

if __name__ == '__main__':
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
