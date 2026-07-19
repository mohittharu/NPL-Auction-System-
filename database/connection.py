import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="npl_auction_system"
)

cursor = conn.cursor()

print("Connected Successfully")