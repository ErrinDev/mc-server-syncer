from dotenv import load_dotenv
import pymysql
import os

pymysql.install_as_MySQLdb()
load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def check_tables_exist(tables):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            for table in tables:
                sql = "SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = %s"
                cursor.execute(sql, (table,))
                result = cursor.fetchone()
                if result['count'] == 0:
                    print(f"Table '{table}' does not exist")
                else:
                    print(f"Table '{table}' exists")