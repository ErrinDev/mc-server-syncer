from dotenv import load_dotenv
import yaml
import threading
import queue
import os
import time
import sys
from modules import database

load_dotenv()

# Queue for messages to display in the CLI
output_queue = queue.Queue()

def load_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

def output(message):
    """Add a message to the output queue"""
    output_queue.put(message)

def check_database():
    """Check database connection and tables, create missing tables"""
    output("Testing database connection...")
    connection_test = database.connection_test()
    
    if connection_test:
        output("Database connection successful")
        try:
            config = load_config()
            tables = config['tables']
            output(f"Checking {len(tables)} tables...")
            
            # Get list of missing tables
            missing_tables = database.check_tables_exist(tables)
            
            # Create missing tables if any
            if missing_tables:
                output(f"\nCreating {len(missing_tables)} missing tables...")
                for table in missing_tables:
                    result = database.create_table(table)
                    if result:
                        output(f"Successfully created table '{table}'")
                    else:
                        output(f"Failed to create table '{table}'")
                
                # Re-check tables after creation
                output("\nVerifying tables after creation...")
                database.check_tables_exist(tables)
            else:
                output("All required tables exist")
                
        except Exception as e:
            output(f"Error while processing tables: {e}")
    else:
        output("Database connection failed. Please check your environment variables and network connectivity")

def output_worker():
    """Worker to display messages from the queue"""
    while True:
        try:
            message = output_queue.get(timeout=0.1)
            # Clear the current line
            sys.stdout.write("\r" + " " * 80 + "\r")
            # Print the message
            print(message)
            # Re-display the prompt
            sys.stdout.write("> ")
            sys.stdout.flush()
            output_queue.task_done()
        except queue.Empty:
            # No messages, continue
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in output worker: {e}")

def input_worker():
    """Worker to handle user input"""
    while True:
        try:
            # Display prompt
            sys.stdout.write("> ")
            sys.stdout.flush()
            
            # Get input
            command = input().strip()
            
            # Process the command
            if command.lower() in ['quit', 'exit', 'q', 'stop']:
                output("Exiting...")
                os._exit(0)

            elif command.lower() == 'help':
                output("Available commands:")
                output("  help - Show this help")
                output("  status - Check database connection status")
                output("  tables - Check database tables")
                output("  exit/quit/stop - Exit the program")

            elif command.lower() == 'status':
                threading.Thread(target=check_database).start()

            elif command.lower() == 'tables':
                def check_tables():
                    try:
                        config = load_config()
                        tables = config['tables']
                        database.check_tables_exist(tables)
                    except Exception as err:
                        output(f"Error checking tables: {err}")
                threading.Thread(target=check_tables).start()
            else:
                output(f"Unknown command: {command}, use 'help' for a list of commands")
        except Exception as e:
            output(f"Error processing command: {e}")

if __name__ == "__main__":
    # Start the output worker thread
    output_thread = threading.Thread(target=output_worker, daemon=True)
    output_thread.start()
    
    # Initial database check in a separate thread
    db_thread = threading.Thread(target=check_database, daemon=True)
    db_thread.start()
    
    # Start the input worker in the main thread
    output("Welcome to MC Server Syncer CLI")
    output("Type 'help' for a list of commands")
    input_worker()

