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
    incident_types = r"(Traffic Stop|Suspicious|Missing Person|Assist Fire|Test Call|Animal Vicious|Preg/Child Birth/Miscarriage|Welfare Check|Bomb/Threats/Package|Special Assignment|Prowler|Burns/Explosions|EMS Mutual Aid|Homicide|Stand By EMS|Loud Party|Molesting|Fire Residential|Cardiac Respritory Arrest|Body Reported|Animal Livestock|Traumatic Injury|Reckless Driving|Shooting Stabbing Penetrating|Carbon Mon/Inhalation/HazMat|Foot Patrol|Transfer/Interfacility|Animal Trapped|Choking|Burglary|COP Relationships|Unknown Problem/Man Down|Officer Needed Nature Unk|Barking Dog|Animal Bites/Attacks|Warrant Service|Contact a Subject|Disturbance/Domestic|Motorist Assist|Noise Complaint|Larceny|Trespassing|Unconscious/Fainting|Medical Call Pd Requested|Shots Heard|Alarm|Supplement Report|Convulsion/Seizure|MVA With Injuries|Overdose/Poisoning|Mutual Aid|Diabetic Problems|Heat/Cold Exposure|Breathing Problems|Public Assist|Runaway or Lost Child|Chest Pain|MVA Non Injury|Public Intoxication|Stroke|Open Door/Premises Check|Check Area|Vandalism|Animal Complaint|Animal Dead|Fire Alarm|Follow Up|Item Assignment|Animal Injured|Fraud|Pick Up Partner|Supplement Report|911 Call Nature Unknown|Falls|Escort/Transport|Animal at Large|Parking Problem|Abdominal Pains/Problems|Indecent Exposure|Animal Bite|Hit and Run|Stolen Vehicle|Sick Person|Harassment / Threats Report|Fire Grass|Assault EMS Needed|Alarm Holdup/Panic|Fight|Fire Smoke Investigation|Heart Problems/AICD|Fire Commercial|Fire Electrical Check|COP DDACTS|Fire Odor Investigation|Extra Patrol|Fire Controlled Burn|Civil Standby|Drunk Driver|Hemorrhage/Lacerations|Warrant Service|Debris in Roadway|Pick Up Items|Found Item|Stand By EMS|Stake Out|Unknown Problem/Man Down|Officer Needed Nature|Assist Police|Unk|Allergies/Envenomations|Road Rage|Fire Carbon Monoxide Alarm|Fire Water Rescue|Fire Down Power Line|Fire Gas Leak|Drowning/Diving/Scuba Accident|Cardiac Respiratory Arrest|Drug Violation|Loud Party)"
    ori_types = r"(OK0140200|14005|EMSSTAT)"
    incident_pattern = rf"(\d{{1,2}}/\d{{1,2}}/\d{{4}} \d{{1,2}}:\d{{2}})\s+(\d{{4}}-\d{{8}})\s+(.*?)(?:(\n(?!\d{{1,2}}/\d{{1,2}}/\d{{4}}).*)+)?\s+({incident_types})\s+({ori_types})"
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text() +"\n"
    lines = text.splitlines()

    extracted_data = []
    current_location = ''
    for line in lines:
        if "Daily Incident Summary (Public)" in line or line is None or "Date / Time Incident Number Location Nature Incident ORI" in line:
            continue

        # Check if the line starts a new incident
        if re.match(r'\d{1,2}/\d{1,2}/\d{4}', line):

            line = re.sub(r'(\d{4}-\d{8})([A-Z])', r'\1 \2', line)
            match = re.match(incident_pattern, line)
            if match:
                data_ = match.groups()
                extracted_data.append([data_[0], data_[1], data_[2], data_[4], data_[6]])  
            current_location = line 

        else:
            line = current_location + ' ' + line
            line = re.sub(rf'{incident_types}', r' \1', line)
            match = re.match(incident_pattern, line)
            if match:
                data_ = match.groups()
                extracted_data.append([data_[0], data_[1], data_[2], data_[4], data_[6]])  

    return extracted_data
def createdb(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''
    DROP TABLE IF EXISTS incidents
    ''')

    # Create incidents table
    cur.execute('''
    CREATE TABLE incidents (
    incident_time TEXT,
    incident_number TEXT,
    incident_location TEXT,
    nature TEXT,
    incident_ori TEXT
    );''')

    conn.commit()
    conn.close()

# Function to populate the SQLite database with extracted data
def populatedb(db, incidents):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Insert data into the database
    cur.executemany('''
    INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
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
    ORDER BY nature
    ''')

    nature_counts = cur.fetchall()
    for nature, count in nature_counts:
        print(f"{nature}|{count}")

    conn.close()


