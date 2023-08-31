from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import subprocess
import csv
import time

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_data = None
    website_urls = []
    processing_status = False  # Initialize processing status

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Start processing status
            processing_status = True

            # Run the getting_data.py file using subprocess
            subprocess.run(['python3', 'getting_data.py', file_path])

            # Read the combined_results.csv file and store its data
            uploaded_data = read_csv_data('combined_results.csv')

            # Extract website URLs from the data
            website_urls = [row[2] for row in uploaded_data]

            # End processing status
            processing_status = False

    return render_template('index.html', uploaded_data=uploaded_data, website_urls=website_urls, processing_status=processing_status)

@app.route('/check_processing', methods=['GET'])
def check_processing():
    # Simulate processing time
    time.sleep(2)  # Sleep for 2 seconds (you can adjust this)

    # Return a JSON response indicating processing status
    processing_status = False  # Change this based on your processing logic
    return jsonify({'processing': processing_status})

def read_csv_data(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

if __name__ == '__main__':
    app.run(debug=True)
