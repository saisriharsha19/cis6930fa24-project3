from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt
import os, io
import pandas as pd
from func import extractincidents, createdb, populatedb, fetchincidents
from visualization import create_visualizations

app = Flask(__name__)
DB_PATH = 'resources/normanpd.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('files')
    urls = request.form.get('urls')

    if not uploaded_files and not urls:
        return "No files or URLs provided", 400

    # Process uploaded files
    for file in uploaded_files:
        if file.filename:
            pdf_file = file.read()
            extracted_data = extractincidents(io.BytesIO(pdf_file))
            createdb(DB_PATH)
            populatedb(DB_PATH, extracted_data)

    # Process URLs
    if urls:
        url_list = urls.splitlines()
        for url in url_list:
            pdf_file = fetchincidents(url)
            extracted_data = extractincidents(pdf_file)
            createdb(DB_PATH)
            populatedb(DB_PATH, extracted_data)

    return redirect(url_for('visualize'))

@app.route('/visualize')
def visualize():
    create_visualizations(DB_PATH)

    return render_template(
        'visualizations.html',
        bar_chart='static/bar_chart.png',
        clustering='static/clustering.png',
        histogram='static/histogram.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
