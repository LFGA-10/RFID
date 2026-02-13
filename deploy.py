
import paramiko
import os
import time

# Credentials
HOST = "157.173.101.159"
USER = "user274"
PASS = "2ZQ@!M7R"
PORT = 22

# Remote Paths
REMOTE_DIR = "rfid_project"
APP_FILE = "app.py"
TEMPLATE_DIR = "templates"
TEMPLATE_FILE = "dashboard_v2.html"

def deploy():
    print(f"Connecting to {HOST}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, port=PORT, username=USER, password=PASS)
        
        sftp = ssh.open_sftp()
        
        # 1. Create Directory
        print("Creating remote directory...")
        try:
            sftp.mkdir(REMOTE_DIR)
        except OSError:
            pass # Directory might exist
            
        try:
            sftp.mkdir(f"{REMOTE_DIR}/{TEMPLATE_DIR}")
        except OSError:
            pass

        # 2. Upload Files
        print("Uploading app.py...")
        sftp.put("app.py", f"{REMOTE_DIR}/{APP_FILE}")
        
        print("Uploading dashboard_v2.html...")
        sftp.put(f"templates/{TEMPLATE_FILE}", f"{REMOTE_DIR}/{TEMPLATE_DIR}/{TEMPLATE_FILE}")
        
        sftp.close()
        
        # 3. Setup & Run
        print("Installing dependencies on VPS...")
        # Using a single command string to ensure context persists if needed, though mostly independent
        # Kill existing process on 9274 if any
        kill_cmd = "fuser -k 9274/tcp" 
        deps_cmd = "pip3 install flask flask-socketio eventlet paho-mqtt"
        run_cmd = f"cd {REMOTE_DIR} && nohup python3 {APP_FILE} > output.log 2>&1 &"
        
        # We execute commands sequentially
        stdin, stdout, stderr = ssh.exec_command(deps_cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("Dependencies installed.")
        else:
            print("Error installing dependencies:", stderr.read().decode())
        
        # Kill old process
        ssh.exec_command(kill_cmd)
        time.sleep(2) # Wait for kill
        
        # Start new process
        print("Starting application...")
        ssh.exec_command(run_cmd)
        
        print("Deployment triggered. Waiting a few seconds to verify...")
        time.sleep(5)
        
        # Check if it's running
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep app.py")
        print("Process check:", stdout.read().decode())
        
        ssh.close()
        print(f"Deployment Complete! Access at http://{HOST}:9274")
        
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    deploy()
