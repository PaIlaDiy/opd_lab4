from flask import Flask, request, render_template
from collections import Counter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                words = content.split()
                word_counts = Counter(words)
                most_common_word, count = word_counts.most_common(1)[0]
                return f"The most common word is '{most_common_word}' with {count} occurrences."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)