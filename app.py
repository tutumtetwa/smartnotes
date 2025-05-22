from flask import Flask, render_template, request
import spacy

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
    app.run(debug=True)
