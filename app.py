from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from VoiceToText import recognize_speech
from pdfextract import PDFExtract
from model import get_most_relevant_sentences

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set maximum upload size to 16MB

pdf_extractor = PDFExtract()

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        global pdf_text_list
        pdf_text_list = pdf_extractor.process_pdf(file_path)
        return '', 200

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    relevant_sentences = get_most_relevant_sentences(user_input, pdf_text_list)
    return jsonify(relevant_sentences)

if __name__ == "__main__":
    app.run(debug=True)
