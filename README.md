## *Features*

### 1. **Data Processing**:
   - Parse and clean SMS data from an XML file.
   - Categorize transactions into types such as Incoming Money, Payments, Transfers, etc.
   - Log any unprocessed or erroneous data into a separate file for troubleshooting.

### 2. **Database**:
   - Designed a normalized relational database schema to store transaction data.
   - Populated the database with cleaned and categorized data.

### 3. **Frontend Dashboard**:
   - Interactive dashboard built with HTML, CSS, and JavaScript.
   - Features include:
     - Search and filter transactions by type, date, or amount.
     - Visualizations (bar charts, pie charts) to represent transaction volume and distribution.
     - Detailed view of individual transactions.
   - The frontend fetches data in JSON format directly from the database (no Flask API involved).

### 4. **Backend (Data Processing)**:
   - The backend processes the SMS data and populates the database directly without using a server (no Flask API).
   - Transaction data is fetched using JavaScript's Fetch API in JSON format and presented in the frontend.

---

## *Technologies Used*

- **Backend**: Python (xml.etree.ElementTree, sqlite3).
- **Frontend**: HTML, CSS, JavaScript (Chart.js for data visualization), Fetch API (for retrieving data in JSON format).
- **Database**: SQLite.
- **Version Control**: Git and GitHub.

---

## *How to Run the Application*

### 1. **Clone the Repository**:
   Clone the project to your local machine:
   ```bash
   git clone https://github.com/your_user/repo_name
   cd repo_name

## 2. Set Up the Backend:**
Install necessary dependencies:

pip install -r requirements.txt
Run the Python script to process the SMS data and populate the database:
python backend/populate_db.py

## 3. Launch the Frontend:
Open the frontend/index.html file in your browser. The frontend will automatically fetch transaction data in JSON format from the backend and display it in interactive charts and tables.

This `README.md` is structured for clarity and includes all the instructions and details about setting up and running the application. You can now add this file to your project repository, and it will be ready for others to use.


