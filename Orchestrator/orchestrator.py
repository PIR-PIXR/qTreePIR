import os
import sys
import math
import random
import shutil
import paramiko
import subprocess
from scp import SCPClient

# Define constants
HOME_PATH = "/qTreePIR"
SERVER_PATH = "/home/ubuntu"
SERVER_NAME = "ubuntu"
PRIVKEY_FILE = "rmit.pem"
ATC_PATH = os.path.join(HOME_PATH, "ATC")
PBC_PATH = os.path.join(HOME_PATH, "PBC")
LOG_PATH = os.path.join(HOME_PATH, "Logs")
SEALPIR_PATH = os.path.join(HOME_PATH, "ParallelSealPIR")
ORCHESTRATOR_PATH = os.path.join(HOME_PATH, "Orchestrator")
AWSKEY_PATH = os.path.join(HOME_PATH, "AWSkey")

def run_ATC(h, q):
    java_file_path = os.path.join(ATC_PATH, "ATC.java")
    gson_jar_path = os.path.join(ATC_PATH, "gson-2.10.1.jar")
    classpath = f'{gson_jar_path}:{ATC_PATH}'
    main_class_name = 'ATC'

    subprocess.run(['javac', '-cp', gson_jar_path, java_file_path], check=True) # Compile Java source code
    subprocess.run(['java', '-cp', classpath, main_class_name, str(h), str(q)], check=True)  # Run compiled Java class
    #subprocess.run(['java', '-Xmx120g','-cp', classpath, main_class_name, str(h), str(q)], check=True)  # Run compiled Java class

def read_servers_ip():
    file_path = os.path.join(ORCHESTRATOR_PATH, 'list_servers_IPs.txt')
    try:
        with open(file_path, 'r') as file:
            ip_addresses = file.read().split()
        return ip_addresses
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

# Sent file from local machine to server
def send_file_to_server(server_ip, username, privkey_path, local_path, server_path):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        ssh.connect(server_ip, username=username, key_filename=privkey_path)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_path, server_path)
        ssh.close()

        print(f"File successfully sent from {local_path} to {server_ip}:{server_path}")
    except Exception as e:
        print(f"Error transferring file from {local_path} to {server_ip}:{server_path}: {e}")

# Sent file from server to local machine
def receive_file_from_server(server_ip, username, privkey_path, local_path, server_path):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        ssh.connect(server_ip, username=username, key_filename=privkey_path)

        with SCPClient(ssh.get_transport()) as scp:
            scp.get(server_path, local_path)

        # Remove the remote file after successful download
        ssh.exec_command(f"rm {server_path}")

        # Close the SSH connection
        ssh.close()

        print(f"File successfully received from {server_ip}:{server_path} to {local_path}")
        print(f"Remote file {server_path} deleted.")
    except Exception as e:
        print(f"Error transferring file from {server_ip}:{server_path} to {local_path}: {e}")

def copy_and_remove_file(src_path, dest_path):
    try:
        # Copy the file from source to destination
        shutil.copy(src_path, dest_path)
        print(f"File '{src_path}' copied to '{dest_path}'.")
        # Remove the original file
        os.remove(src_path)
        print(f"Original file '{src_path}' removed.")
    except FileNotFoundError:
        print(f"Error: File '{src_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Read indices from the file created by ATC
def read_indices_from_file(file_path):
    entries = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        entry = None
        for line in lines:
            if line.startswith('TX_index:'):
                if entry is not None:
                    entries.append(entry)

                # Create a new entry
                entry = {'TX_index': int(line.split(':')[1].strip()), 'file_entries': []}
            else:
                # Extract information from lines
                parts = line.split(';')
                if len(parts) == 3:
                    file_info = {
                        'FileName': parts[0].strip(),
                        'NodeID': int(parts[1].split(':')[1].strip()),
                        'Index': int(parts[2].split(':')[1].strip())
                    }
                    entry['file_entries'].append(file_info)

        # Add the last entry if it exists
        if entry is not None:
            entries.append(entry)

    return entries

def generate_servers_list(server_ips, entries, output_file_path):
    with open(output_file_path, 'w') as file:
        for entry in entries:
            i = 0
            for file_entry in entry['file_entries']:
                server_ip = server_ips[i] if server_ips else "127.0.0.1"
                i += 1
                port_number = 3000  # You can replace this with your port number
                file_name = file_entry['FileName']
                index = file_entry['Index']

                # Write to the file
                file.write(f"{server_ip}:{port_number};{file_name};{index}\n")

    print(f"Servers_list successfully saved to {output_file_path}")

def build_parallel_SealPIR():
    os.chdir(SEALPIR_PATH)
    subprocess.run(["cmake", "."])
    subprocess.run(["make"])

def run_SealPIR_client():
    os.chdir(SEALPIR_PATH)
    # Run pirmessage_client
    subprocess.run(["./pirmessage_client"], check=True)
    print("pirmessage_client successfully executed")

def run_SealPIR_server(server_ip, privkey_path, port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to the remote server
    ssh.connect(server_ip, username=SERVER_NAME, key_filename=privkey_path)

    # Run pirmessage_server on the remote server with the specified port
    command = f"cd {SERVER_PATH} && rm server_log.txt"
    ssh.exec_command(command)
    command = f"cd {SERVER_PATH} && ./pirmessage_server -port {port}"
    ssh.exec_command(command)

    print("pirmessage_server successfully sent and executed on the remote server")

    ssh.close()

def generate_random_TX_index(num_values):

    if len(sys.argv) >= 3:
        h = int(sys.argv[1])
        q = int(sys.argv[2])

    path = os.path.join(ORCHESTRATOR_PATH, f"list_TXs_{h}_{q}.txt")

    # Function to generate a random j value in the range [1, q^h]
    def random_j(q, h):
        return random.randint(1, int(math.pow(q, h)))

    # Generate random TX indices
    random_TX_indicies = [random_j(q, h) for _ in range(num_values)]

    # Save the values in the specified file
    with open(path, "w") as file:
        for value in random_TX_indicies:
            file.write(str(value) + "\n")
    # Copy the file from source to destination
    shutil.copy(path, ATC_PATH)
    # Copy the file from source to destination
    shutil.copy(path, PBC_PATH)

    print(f"{num_values} random TX indices saved in {path}")


def color_parallel_SealPIR(h, q):
    color = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    privkey_path = os.path.join(AWSKEY_PATH, PRIVKEY_FILE)

    # Run the ATC
    print("Running ATC_db: Setup Color databases...")
    run_ATC(h, q)

    # Read Servers' IP and send color databases to each server
    server_ips = read_servers_ip()
    for i in range(h):
        print(f"Server address: {server_ips[i]}")
        local_file_path = os.path.join(ATC_PATH, f"color{color[i]}_{h}_{q}.json")
        send_file_to_server(server_ips[i], SERVER_NAME, privkey_path, local_file_path, SERVER_PATH)

    # Read indices
    color_indices_path = os.path.join(ORCHESTRATOR_PATH, f"color_indices_{h}_{q}.txt")
    output_file_path = os.path.join(SEALPIR_PATH, "servers_list.txt")
    entries = read_indices_from_file(color_indices_path)

    # Generate servers_list.txt
    generate_servers_list(server_ips, entries, output_file_path)

    # Build SealPIR for client and servers
    build_parallel_SealPIR()

    # Send pirmessage_server to each server
    local_file_path = os.path.join(SEALPIR_PATH, 'pirmessage_server')
    for i in range(h):
        print(f"Server address: {server_ips[i]}")
        send_file_to_server(server_ips[i], SERVER_NAME, privkey_path, local_file_path, SERVER_PATH)
        # Run SealPIR Servers
        run_SealPIR_server(server_ips[i], privkey_path, 3000)

    # Run SealPIR Client
    run_SealPIR_client()

    # Transfer logs from servers to local machine
    for i in range(h):
        local_file_path = os.path.join(LOG_PATH, f"color{color[i]}_{h}_{q}_log.txt")
        receive_file_from_server(server_ips[i], SERVER_NAME, privkey_path, local_file_path, os.path.join(SERVER_PATH, "server_log.txt"))

    # Transfer log files from source to Logs path
    src_path = os.path.join(ATC_PATH, f"ATC_{h}_{q}_log.txt")
    dest_path = os.path.join(LOG_PATH, f"ATC_{h}_{q}_log.txt")
    copy_and_remove_file(src_path, dest_path)

    src_path = os.path.join(ATC_PATH, f"ATCindexing_{h}_{q}_log.txt")
    dest_path = os.path.join(LOG_PATH, f"ATCindexing_{h}_{q}_log.txt")
    copy_and_remove_file(src_path, dest_path)

    src_path = os.path.join(SEALPIR_PATH, "client_log.txt")
    dest_path = os.path.join(LOG_PATH, f"color_client_{h}_{q}_log.txt")
    copy_and_remove_file(src_path, dest_path)

    src_path = os.path.join(ORCHESTRATOR_PATH, f"color_indices_{h}_{q}.txt")
    dest_path = os.path.join(LOG_PATH, f"color_indices_{h}_{q}.txt")
    copy_and_remove_file(src_path, dest_path)


def run_PBC(h, q):
    # Change the working directory to the project directory
    os.chdir(PBC_PATH)
    cmake_configure_cmd = "cmake -S . -B build"
    subprocess.run(cmake_configure_cmd, shell=True, check=True)
    cmake_build_cmd = "cmake --build build"
    subprocess.run(cmake_build_cmd, shell=True, check=True)

    # Initialize PBC databases, map
    server_cmd = f"./build/bin/vectorized_batch_pir server {h} {q} {PBC_PATH}"
    subprocess.run(server_cmd, shell=True, check=True)

    # Initialize queries
    client_cmd = f"./build/bin/vectorized_batch_pir client {h} {q} {PBC_PATH}"
    subprocess.run(client_cmd, shell=True, check=True)

def pbc_parallel_SealPIR(h, q):
    privkey_path = os.path.join(AWSKEY_PATH, PRIVKEY_FILE)

    # Run the PBC
    print("Running PBC_db: Setup PBC databases...")
    run_PBC(h, q)

    # Read Servers' IP and send PBC databases to each server
    server_ips = read_servers_ip()
    for i in range(math.ceil(1.5 * h)):
        print("Server address: " + server_ips[i])
        local_file_path = os.path.join(PBC_PATH, f"PBC_data/PBC{i+1}_{h}_{q}.json")
        send_file_to_server(server_ips[i], SERVER_NAME, privkey_path, local_file_path, SERVER_PATH)

    # Read indices
    pbc_indices_path = os.path.join(PBC_PATH, f"requests/pbc_indices_{h}_{q}.txt")
    output_file_path = os.path.join(SEALPIR_PATH, "servers_list.txt")
    entries = read_indices_from_file(pbc_indices_path)
    # Generate servers_list.txt
    generate_servers_list(server_ips, entries, output_file_path)

    # Build SealPIR for client and servers
    build_parallel_SealPIR()

    # Send pirmessage_server to each server
    local_file_path = os.path.join(SEALPIR_PATH, 'pirmessage_server')
    for i in range(math.ceil(1.5 * h)):
        print("Server address: " + server_ips[i])
        send_file_to_server(server_ips[i], SERVER_NAME, privkey_path, local_file_path, SERVER_PATH)
        # Run SealPIR Servers
        run_SealPIR_server(server_ips[i], privkey_path, 3000)

    # Run SealPIR Client
    run_SealPIR_client()

    # Construct remote and local file paths
    server_file_path = os.path.join(SERVER_PATH, "server_log.txt")

    # Sent logs from servers to local machine
    for i in range(math.ceil(1.5 * h)):
        local_file_path = os.path.join(LOG_PATH, f"pbc{i+1}_{h}_{q}_log.txt")
        receive_file_from_server(server_ips[i], SERVER_NAME, privkey_path, local_file_path, server_file_path)

    # Sent log files from the source to Logs path
    src_path = os.path.join(SEALPIR_PATH, "client_log.txt")
    dest_path = os.path.join(LOG_PATH, f"pbc_client_{h}_{q}_log.txt")
    copy_and_remove_file(src_path, dest_path)

    src_path = os.path.join(PBC_PATH,  f"client_log/client_{h}_{q}.txt")
    dest_path = os.path.join(LOG_PATH, f"pbc_indexing_{h}_{q}_log.txt")
    copy_and_remove_file(src_path, dest_path)

    src_path = os.path.join(PBC_PATH, f"server_log/server_{h}_{q}.txt")
    dest_path = os.path.join(LOG_PATH, f"PBC_{h}_{q}_log.txt")
    copy_and_remove_file(src_path, dest_path)

    src_path = os.path.join(PBC_PATH, f"requests/pbc_indices_{h}_{q}.txt")
    dest_path = os.path.join(LOG_PATH, f"pbc_indices_{h}_{q}.txt")
    copy_and_remove_file(src_path, dest_path)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        h = int(sys.argv[1])
        q = int(sys.argv[2])

        generate_random_TX_index(1)

        color_parallel_SealPIR(h, q)

        #pbc_parallel_SealPIR(h, q)

        print("Orchestration completed successfully.")
    else:
        print("Insufficient command-line arguments. Usage: python3 orchestrator.py <parameter1: (h)> <parameter2: (q)>")
