from typing import List

from dotenv import load_dotenv
import pymysql
import os

pymysql.install_as_MySQLdb()
load_dotenv()

def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    
def connection_test() -> bool:
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
    except pymysql.err.OperationalError as e:
        print(f"Database connection error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def create_table(name: str) -> bool:
    print(f"Creating table '{name}'...")
    connection = get_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = f"""
                CREATE TABLE {name} (
                    key_name VARCHAR(255) PRIMARY KEY,
                    value_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql)
                print(f"Table '{name}' created successfully")
                return True
    except Exception as e:
        print(f"Error creating table '{name}': {e}")
        return False


def check_tables_exist(tables: List[str]) -> List[str]:
    table_missing_list = []
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            for table in tables:
                # Check if table exists
                sql = "SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = %s"
                cursor.execute(sql, (table,))
                result = cursor.fetchone()

                if result['count'] == 0:
                    print(f"Table '{table}' does not exist")
                    table_missing_list.append(str(table))
                else:
                    print(f"Table '{table}' exists")
                    
                    # Count rows in the table
                    try:
                        row_sql = f"SELECT COUNT(*) as row_count FROM {table}"
                        cursor.execute(row_sql)
                        row_result = cursor.fetchone()
                        print(f"  - Rows in '{table}': {row_result['row_count']}")
                    except Exception as e:
                        print(f"  - Error counting rows in '{table}': {e}")
    
    return table_missing_list