# Importing required packages
import pandas as pd         # pip install pandas                    (Data Manipulation)
import mysql.connector      # pip install mysql-connector-python    (MySQL Connector)
# pip install openpyxl                                              (Reading Excel File)

# Read Excel file into a DataFrame
df = pd.read_excel('StudentData.xlsx')

# Connect to MySQL Database
dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='TIGER',
)

cursorObject = dataBase.cursor()

# Create Database
cursorObject.execute("CREATE DATABASE IF NOT EXISTS demodb")
cursorObject.execute("USE demodb")

# Create Table
query = "CREATE TABLE Student_Data (Enrollment_No VARCHAR(11), Name VARCHAR(255), Gender VARCHAR(6), Mobile_No VARCHAR(10), Email_Address VARCHAR(25), Aadhar_Card VARCHAR(10), Branch VARCHAR(25), Semester VARCHAR(2));"
cursorObject.execute(query)

# Insert Data into Table
query = 'INSERT INTO Student_Data (Enrollment_No, Name, Gender, Mobile_No, Email_Address, Aadhar_Card, Branch, Semester) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

# Iterate through DataFrame and execute INSERT query for each row
for row in df.itertuples():
    cursorObject.execute(query, (row.Enrollment_No, row.Name, row.Gender, row.Mobile_No, row.Email_Address, row.Aadhar_Card, row.Branch, row.Semester))

# Commit changes to the database
dataBase.commit()

# Close cursor and database connection
cursorObject.close()
dataBase.close()

print("Data Entered Successful!")