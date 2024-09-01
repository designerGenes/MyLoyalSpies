import socket
import paramiko
import re
import webbrowser
import time

BEACON_PORT = 5005
BEACON_MESSAGE = b"VIDEO_SERVER_BEACON"

def listen_for_beacon(timeout=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', BEACON_PORT))
    sock.settimeout(timeout)

    print(f"Listening for video server beacon for {timeout} seconds...")
    try:
        data, addr = sock.recvfrom(1024)
        if data == BEACON_MESSAGE:
            return addr[0]
    except socket.timeout:
        pass
    return None

def check_ssh(ip, key_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username='pi', key_filename=key_path, timeout=5)
        return ssh
    except:
        return None

def get_flask_port(ssh):
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep 'python.*flask'")
    output = stdout.read().decode()
    match = re.search(r'port=(\d+)', output)
    if match:
        return match.group(1)
    return None

def main():
    key_path = '~/.ssh/MyLoyalSpies_Viewer'

    while True:
        server_ip = listen_for_beacon()
        if server_ip:
            print(f"Detected video server at {server_ip}")
            ssh = check_ssh(server_ip, key_path)
            if ssh:
                print(f"Successfully connected to {server_ip}")
                port = get_flask_port(ssh)
                ssh.close()

                if port:
                    url = f"http://{server_ip}:{port}"
                    print(f"Flask server found at {url}")
                    webbrowser.open(url)
                    return
                else:
                    print("Flask server not running on this host.")
            else:
                print(f"Could not establish SSH connection to {server_ip}")
        else:
            print("No video server beacon detected. Retrying...")
        
        time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()
