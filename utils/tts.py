import os, time
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import uuid
import textwrap
import hashlib
from flask import Blueprint, request, jsonify
from utils.tts_utils import generate_mp3  


voice_bp = Blueprint('voice', __name__)

def clean_old_audio_files():
    audio_dir = os.path.join('static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    now = time.time()
    for file in os.listdir(audio_dir):
        path = os.path.join(audio_dir, file)
        if os.path.isfile(path) and now - os.path.getmtime(path) > 600:
            os.remove(path)



@voice_bp.route('/voice', methods=['POST'])
def voice():
    summary = request.form.get('summary', '')
    if not summary:
        return jsonify({'error': 'No summary provided'}), 400

    # Generate hash for filename
    hash = hashlib.md5(summary.encode()).hexdigest()
    output_path = os.path.join('static', 'audio', f"summary_{hash}.mp3")

    # Only generate if it doesn't exist already
    if not os.path.exists(output_path):
        generate_mp3(summary, output_path)  # This should generate and save the mp3

    return jsonify({'audio_url': f'/static/audio/summary_{hash}.mp3'})



def generate_mp3(text, output_path):
    chunks = textwrap.wrap(text, 200, break_long_words=False)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    combined = AudioSegment.empty()

    for chunk in chunks:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as tf:
            gTTS(text=chunk).save(tf.name)
            segment = AudioSegment.from_file(tf.name)
            combined += segment

    combined.export(output_path, format="mp3")

