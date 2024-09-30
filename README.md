# cis6930fa24-project0

README
Name: Sai Sri Harsha Guddati
Assignment Description
This project involves downloading, extracting, and processing incident data from a PDF available online. The incident data is extracted and processed, and stored in an SQLite database. Additionally, the assignment involves displaying a statistical summary of the incident types.

Fetching PDF: Download a PDF file containing incident summaries from the given URL.
Extracting Incidents: Extract key information from the PDF, including date, incident number, location, nature of the incident, and the ORI (Originating Agency Identifier).
Database Creation: Create an SQLite database to store the incident data.
Data Insertion: Populate the database with the extracted incidents.
Displaying Statistics: Output a count of incidents, grouped by their nature, to the console.
Testing: The functionality of each part is verified using unit tests.
How to Install
To install the required dependencies, ensure you have pipenv installed. Navigate to the project directory and run:

bash
Copy code
pipenv install -e .
This will install all the necessary dependencies in an isolated environment.

How to Run
Fetching and Storing Incidents
You can run the project by specifying the URL of the incident summary PDF:

bash
Copy code
pipenv run python main.py --incidents <incident-summary-url>
This will download the PDF, extract the data, create a local SQLite database, and display the incident nature statistics.

Testing
To run the test suite:

bash
Copy code
pipenv run python -m pytest -v
The test files are located in the tests/ folder, ensuring that the critical functions work as expected.

Example Output
After running the code with an incident PDF, the following output will be printed as an example of the statistical summary:

python
Copy code
Abdominal Pains/Problems | 5
Alarm | 10
Animal Complaint | 3
Assault EMS Needed | 1
...
Functions Overview
Main File
main.py The main file contains the main() function which orchestrates the fetching, extracting, and processing of the incident data. The script is designed to be run from the command line, with arguments provided for the incident summary URL.

fetchincidents(url): Downloads the incident summary PDF from the given URL.
extractincidents(pdf_file): Extracts the incidents from the downloaded PDF file.
createdb(db): Creates an SQLite database with a table for storing incidents.
populatedb(db, incidents): Inserts the extracted incidents into the database.
status(db): Displays statistics of incidents, grouped by their nature, to the console.
Test Files
test_fetch_data_from_api.py This file tests the fetchincidents() function by mocking a PDF file download using the requests module.

test_fetchincidents(): Ensures that the function fetches and returns the correct content type (BytesIO) for a valid URL.
test_extractincidents(): Verifies that the incident extraction logic works correctly, parsing the relevant data fields.
test_process_data.py This file contains tests for verifying database operations:

test_createdb(): Ensures the SQLite database and incidents table are created properly.
test_populatedb(): Confirms that the incident data is correctly inserted into the database.
Bugs and Assumptions
Error Handling: If the URL provided is invalid or the PDF cannot be downloaded, the script raises an exception. There's no specific error handling for malformed URLs.
File Format: The script assumes the PDF file follows the same format as expected for proper incident extraction.
