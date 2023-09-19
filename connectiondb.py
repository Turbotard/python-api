import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python_api",
    port="3306"
)

# faire quelque chose d'utile avec la connexion

db.close()
