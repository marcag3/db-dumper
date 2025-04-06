from flask import Flask
import subprocess
from config import CONFIG

app = Flask(__name__)

@app.route('/dump', methods=['POST'])
def trigger_dump():
    try:
        for db_config in CONFIG["databases"]:
            if db_config["type"] == "mysql":
                dump_command = [
                    "mysqldump",
                    "-h", db_config["host"],
                    "-u", db_config["username"],
                    f"-p{db_config['password']}",
                    db_config["database"],
                    "-r", f"/db_dumps/{db_config['host']}_dump.sql"
                ]
            elif db_config["type"] == "mariadb":
                dump_command = [
                    "mariadb-dump",
                    "-h", db_config["host"],
                    "-U", db_config["username"],
                    "-d", db_config["database"],
                    "-f", f"/db_dumps/{db_config['host']}_dump.sql"
                ]
            elif db_config["type"] == "postgresql":
                dump_command = [
                    "pg_dump",
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
        return f"Dump failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
