from dotenv import load_dotenv
import mysql.connector
import os

#setup
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
    )


if __name__ == "__main__":
