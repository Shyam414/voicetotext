# app.py

from flask import Flask, request, render_template, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_voice():
    if 'voice' not in request.files:
        return jsonify({'error': 'No voice file part'}), 400
    
    voice_file = request.files['voice']
    if voice_file.filename == '':
        return jsonify({'error': 'No selected voice file'}), 400
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(voice_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not transcribe the voice'}), 400
        except sr.RequestError as e:
            return jsonify({'error': f'Could not request results; {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
