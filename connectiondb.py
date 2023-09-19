import mysql.connector

db = mysql.connector.connect(
    host="localhost:3306",
    user="root",
    password="",
    database="python_api",
)

# faire quelque chose d'utile avec la connexion

db.close()
