# cis6930fa24-project0

# README

# Name: Sai Sri Harsha Guddati
## Assignment Description
This project involves downloading, extracting, and processing incident data from a PDF available online. The incident data is extracted and processed, and stored in an SQLite database. Additionally, the assignment involves displaying a statistical summary of the incident types.

1. Fetching PDF: Download a PDF file containing incident summaries from the given URL.
2. Extracting Incidents: Extract key information from the PDF, including date, incident number, location, nature of the incident, and the ORI.
3. Database Creation: Create an SQLite database to store the incident data.
4. Data Insertion: Populate the database with the extracted incidents.
5. Displaying Statistics: Output a count of incidents, grouped by their nature, to the console.
6. Testing: The functionality of each part is verified using unit tests.

## How to Install
To install the required dependencies, ensure you have pipenv installed. Navigate to the project directory and run:

```bash 
pipenv install -e .
```
This will install all the necessary dependencies in an isolated environment.

## How to Run
Fetching and Storing Incidents
You can run the project by specifying the URL of the incident summary PDF:

```bash 
pipenv run python main.py --incidents <incident-summary-url>
```
Here is an example video of running the code using a valid URL.
![run.gif](https://github.com/saisriharsha19/cis6930fa24-project0/blob/main/run.gif)

This will download the PDF, extract the data, create a local SQLite database, and display the incident nature statistics.

## Testing
To run the test files in the /tests/ folder

```bash
pipenv run python -m pytest -v
```

The test files are located in the tests/ folder, ensuring that the critical functions work as expected.

## Example Output
After running the code with an incident PDF, the following output will be printed as an example of the statistical summary:

```python 
911 Call Nature Unknown|1
Abdominal Pains/Problems|4
Alarm|7
Allergies/Envenomations|2
Animal Bite|1
Animal Complaint|4
Animal Dead|2
Animal Injured|1
...
```
## Functions Overview
Main File
### main.py The main file contains the main() function which orchestrates the fetching, extracting, and processing of the incident data. The script is designed to be run from the command line, with arguments provided for the incident summary URL.
### func.py The functions file contains all the code necessary for executing the pipeline. It contains the following functions,
#### fetchincidents(url): Downloads the incident summary PDF from the given URL.
```python
def fetchincidents(url):
    return "Extracted PDF Document"
```
#### extractincidents(pdf_file): Extracts the incidents from the downloaded PDF file.
```python
def extractincidents(pdf_file):
    return "Extracted Incidents"
```
#### createdb(db): Creates an SQLite database with a table for storing incidents.
```python
def createdb(db):
    return "Creates DB named normanpd"
```
#### populatedb(db, incidents): Inserts the extracted incidents into the database.
```python
def populatedb(db, incidents):
    return "Populates the DB with respective fields from extracted data"
```
#### status(db): Displays statistics of incidents, grouped by their nature, to the console.
```python
def status(db):
    return "Displays Nature with number of times they occured"
```
## Test Files
### test_download.py This file tests the fetchincidents() function by mocking a PDF file download using the requests module.

#### test_fetchincidents(): Ensures that the function fetches and returns the correct content type (BytesIO) for a valid URL.
```python
def test_fetchincidents():
    pass
```
#### test_extractincidents(): Verifies that the incident extraction logic works correctly, parsing the relevant data fields.
```python
def test_extractincidents():
    pass
```
### test_random.py This file contains tests for verifying database operations:

### test_createdb(): Ensures the SQLite database and incidents table are created properly.
```python
def test_createdb():
    pass
```
### test_populatedb(): Confirms that the incident data is correctly inserted into the database.
```python
def test_populatedb():
    pass
```
### test_status(self): Checks the output is being printed correct
```python
def test_status(self):
    pass
```
## Database Development
1. Created a Database named "normandb".
2. Created a Table named "incidents" in the DB.
3. If table exixts, delete the table and then create a new table named the same.
4. The incidents table consists of 5 columns named 
    incident_time TEXT,
    incident_number TEXT,
    incident_location TEXT,
    nature TEXT and
    incident_ori TEXT
5. Values are inserted using executemany() option in SQLite.
6. Respective columns are fetched along with their frequencies in the last step.


## Bugs and Assumptions
1. Error Handling: If the URL provided is invalid or the PDF cannot be downloaded, the script raises an exception. There's no specific error handling for malformed URLs.
2. File Format: The script assumes the PDF file follows the same format as expected for proper incident extraction.
3. Regex: The regex only works for the cases that matches with the list of ORI's and Natures that has been placed inside the regex, otherwise it might not match as expected.
