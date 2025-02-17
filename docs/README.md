# MoMo Data Analysis - Fullstack Application

This project is a fullstack application designed to process, analyze, and visualize SMS transaction data from MTN MoMo. The application includes a backend for data cleaning and database management, a relational database to store the processed data, and a frontend dashboard for interactive data visualization.

---

## **Features**
1. **Data Processing**:
   - Parse and clean SMS data from an XML file.
   - Categorize transactions into types (e.g., Incoming Money, Payments, Transfers, etc.).
   - Log unprocessed or erroneous data into a separate file.

2. **Database**:
   - Designed a normalized relational database schema.
   - Populated the database with cleaned and categorized data.

3. **Frontend Dashboard**:
   - Interactive dashboard built with HTML, CSS, and JavaScript.
   - Features include:
     - Search and filter transactions by type, date, or amount.
     - Visualizations (bar charts, pie charts) for transaction volume and distribution.
     - Detailed view of individual transactions.

4. **Backend API (Optional)**:
   - Developed a RESTful API using Flask to fetch data from the database for the frontend.

---

## **Technologies Used**
- **Backend**: Python (Flask, `xml.etree.ElementTree`, `sqlite3`).
- **Frontend**: HTML, CSS, JavaScript (Chart.js for visualizations).
- **Database**: SQLite.
- **Version Control**: Git and GitHub.

---

## **How to Run the Application**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/momo-data-analysis.git
   cd momo-data-analysis

## **Set Up the Backend**:

**Install dependencies**:

bash
Copy
pip install flask
**Run the Flask server**:

bash
Copy
python backend/app.py

## Set Up the Database:

**Run the script to populate the database**:

bash
Copy
python backend/populate_db.py

## **Launch the Frontend**:

Open frontend/index.html in your browser.