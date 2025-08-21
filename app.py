from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import uuid
from werkzeug.utils import secure_filename
from pixel_generator import generate_birthday_card  # ✅ import new function

app = Flask(__name__)
app.secret_key = 'afshah_pixel_birthday_2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected!')
        return redirect(request.url)
    
    file = request.files['file']
    name = request.form.get('name', 'Afshah').strip()
    
    if file.filename == '':
        flash('No file selected!')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        
        input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_input.{file_extension}")
        output_path = os.path.join(OUTPUT_FOLDER, f"{unique_id}_birthday_card.png")
        
        # Save uploaded file (even though we don't really use it here)
        file.save(input_path)

        try:
            # ✅ Generate birthday card with message
            generate_birthday_card(f"🎂 Happy Birthday {name}! 🎉", output_path)

            # Clean up input file
            os.remove(input_path)

            return render_template('result.html',
                                   output_file=f"outputs/{unique_id}_birthday_card.png",
                                   name=name)
        except Exception as e:
            flash(f"Error processing image: {e}")
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload an image file.')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
