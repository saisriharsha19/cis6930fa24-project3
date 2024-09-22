import re
import sqlite3
import requests
from io import BytesIO
from PyPDF2 import PdfReader

# Function to fetch the PDF from a URL
def fetchincidents(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception("Failed to download PDF")

# Function to extract incidents data from the PDF
def extractincidents(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    # Extract text from each page of the PDF
    for page in reader.pages:
        text += page.extract_text()
    
    current_incident = []
    incidents = []

    for line in text:
        line = line.strip()
        
        # Check if the line starts with a date
        if re.match(r'\d+/\d+/\d+ \d+:\d+', line):
            if current_incident:  # If there's an existing incident, save it
                incidents.append(current_incident)
            
            # Start a new incident, split on whitespace
            fields = line.split()
            
            # Determine how many fields were extracted
            if len(fields) >= 5:
                # Assuming the last field is ORI, the rest are other fields
                current_incident = fields[:4] + [' '.join(fields[4:])]  # Combine remaining parts into ORI
            else:
                current_incident = fields  # Just in case there are fewer fields

        else:
            # Handle appending based on current_incident's length
            if len(current_incident) == 3:
                current_incident[2] += ' ' + line  # Append to the location
            elif len(current_incident) == 4:
                current_incident[3] += ' ' + line  # Append to the nature of the incident

        # Save the last incident if it exists
    if current_incident:
        incidents.append(current_incident)
    print(incidents)
    # Print results for verification
    for incident in incidents:
        print(incident)

# Function to create an SQLite database and table
def createdb(db):
    conn = sqlite3.connect('incidents.db')
    cur = conn.cursor()

    # Create incidents table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time TEXT,
        incident_number TEXT,
        location TEXT,
        nature TEXT,
        incident_ori TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Function to populate the SQLite database with extracted data
def populatedb(db, incidents):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Insert data into the database
    cur.executemany('''
    INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori)
    VALUES (?, ?, ?, ?, ?)
    ''', incidents)

    conn.commit()
    conn.close()

# Function to display incident nature statistics
def status(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Query to count occurrences of each nature
    cur.execute('''
    SELECT nature, COUNT(*) 
    FROM incidents 
    GROUP BY nature 
    ORDER BY COUNT(*) DESC
    ''')

    nature_counts = cur.fetchall()
    for nature, count in nature_counts:
        print(f"{nature}: {count} times")

    conn.close()


