import os, time
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import uuid
import textwrap

def clean_old_audio_files():
    audio_dir = os.path.join('static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    now = time.time()
    for file in os.listdir(audio_dir):
        path = os.path.join(audio_dir, file)
        if os.path.isfile(path) and now - os.path.getmtime(path) > 600:
            os.remove(path)



def generate_audio(text):
    # Limit each chunk to ~200 characters
    chunks = textwrap.wrap(text, 200, break_long_words=False)
    output_dir = os.path.join("static", "audio")
    os.makedirs(output_dir, exist_ok=True)

    # Create a unique filename
    filename = f"summary_{uuid.uuid4().hex}.mp3"
    final_path = os.path.join(output_dir, filename)

    combined = AudioSegment.empty()

    for chunk in chunks:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as tf:
            gTTS(text=chunk).save(tf.name)
            segment = AudioSegment.from_file(tf.name)
            combined += segment

    combined.export(final_path, format="mp3")
    return final_path, filename

