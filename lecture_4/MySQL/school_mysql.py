import mysql.connector

config = {
  'user': 'root',
  'password': "${DB_PASSWORD}",
  'host': 'localhost:3306',
  'database': 'inventory',
  'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)