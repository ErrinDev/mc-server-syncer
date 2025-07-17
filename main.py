from dotenv import load_dotenv
import yaml
from modules.database import check_tables_exist

load_dotenv()

def load_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    config = load_config()
    tables = config['tables']
    check_tables_exist(tables)
