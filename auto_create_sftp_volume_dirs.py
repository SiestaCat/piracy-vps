import paramiko, os
#from dotenv import load_dotenv

print("Init...", flush=True)

# READ ENV VARS

#load_dotenv()

SFTP_ADDRESS = os.getenv('SFTP_ADDRESS')
SFTP_PASSWORD = os.getenv('SFTP_PASSWORD')
SFTP_PORT = os.getenv('SFTP_PORT')
SFTP_DOWNLOADS_BASE_FOLDER = os.getenv('SFTP_DOWNLOADS_BASE_FOLDER')
SFTP_CONFIG_BASE_FOLDER = os.getenv('SFTP_CONFIG_BASE_FOLDER')
DOWNLOADS_VOLUMES_FOLDERS = os.getenv('DOWNLOADS_VOLUMES_FOLDERS')
QBITTORRENT_LIST = os.getenv('QBITTORRENT_LIST')

if SFTP_ADDRESS is None:
    raise ValueError("SFTP_ADDRESS is not defined")

if SFTP_PASSWORD is None:
    raise ValueError("SFTP_PASSWORD is not defined")

if SFTP_PORT is None:
    raise ValueError("SFTP_PORT is not defined")

if SFTP_DOWNLOADS_BASE_FOLDER is None:
    raise ValueError("SFTP_DOWNLOADS_BASE_FOLDER is not defined")

if SFTP_CONFIG_BASE_FOLDER is None:
    raise ValueError("SFTP_CONFIG_BASE_FOLDER is not defined")

if DOWNLOADS_VOLUMES_FOLDERS is None:
    raise ValueError("DOWNLOADS_VOLUMES_FOLDERS is not defined")

if QBITTORRENT_LIST is None:
    raise ValueError("QBITTORRENT_LIST is not defined")

# DEFINE DIRS

cmds = []

for qbittorrent_name in QBITTORRENT_LIST.split(','):
    # Config folders
    config_folder = os.path.join(SFTP_CONFIG_BASE_FOLDER, qbittorrent_name)
    cmds.append(f"mkdir -pv \"{config_folder}\"")
    cmds.append(f"touch \"{os.path.join(config_folder, 'dump')}\"")
    # Download folders
    for download_folder_name in DOWNLOADS_VOLUMES_FOLDERS.split(','):
        download_folder = os.path.join(SFTP_DOWNLOADS_BASE_FOLDER, download_folder_name, qbittorrent_name)
        cmds.append(f"mkdir -pv \"{download_folder}\"")
        cmds.append(f"touch \"{os.path.join(download_folder, 'dump')}\"")


# RUN

print("Running...", flush=True)

# Server connection details
username, hostname = SFTP_ADDRESS.split('@')

# Create a new SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(hostname, port=SFTP_PORT, username=username, password=SFTP_PASSWORD)
    for cmd in cmds:
        print(f"Running command {cmd}", flush=True)
        stdin, stdout, stderr = client.exec_command(cmd)
        stdin.close()
        output = stdout.read().decode('utf-8')
        if output:
            print(output, flush=True)
        error = stderr.read().decode('utf-8')
        if error:
            print(f"ERROR: {error}", flush=True)
        else:
            print("OK", flush=True)
finally:
    client.close()  # Ensure closure is in finally block to execute even if the command fails

print("End script")