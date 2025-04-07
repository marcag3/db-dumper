import logging
import traceback
from flask import Flask
import subprocess
from config import CONFIG

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

@app.route('/dump', methods=['POST'])
def trigger_dump():
    try:
        for db_config in CONFIG["databases"]:
            if db_config["type"] == "mysql" or db_config["type"] == "mariadb":
                dump_command = [
                    "/usr/bin/mariadb-dump",
                    "-h", db_config["host"],
                    "-u", db_config["username"],
                    f"-p{db_config['password']}",
                    db_config["database"],
                    "--skip_ssl",
                    "-r", f"/db_dumps/{db_config['host']}_dump.sql"
                ]
            elif db_config["type"] == "postgresql":
                dump_command = [
                    "/usr/bin/pg_dump",
                    "-h", db_config["host"],
                    "-U", db_config["username"],
                    "-d", db_config["database"],
                    "-f", f"/db_dumps/{db_config['host']}_dump.sql"
                ]
            else:
                return f"Unsupported database type: {db_config['type']}", 400

            # Execute the dump command
            subprocess.run(dump_command, check=True, env={"PGPASSWORD": db_config["password"]})
        
        return "All dumps completed successfully", 200
    except subprocess.CalledProcessError as e:
        logging.error("Dump failed: %s", str(e))
        logging.error("Traceback: %s", traceback.format_exc())
        return f"Dump failed: {str(e)}", 500
    except Exception as e:
        logging.error("An unexpected error occurred: %s", str(e))
        logging.error("Traceback: %s", traceback.format_exc())
        return f"An unexpected error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
