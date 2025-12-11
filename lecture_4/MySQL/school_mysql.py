import mysql.connector
import os

config = {
  'user': 'root',
  'password': os.getenv('DB_PASSWORD'),
  'host': 'localhost:3306',
  'database': 'inventory',
  'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)