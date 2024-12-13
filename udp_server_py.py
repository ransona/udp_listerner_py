import os
import shutil
import socket

# Define the server address and port
# Placeholder for server address, to be updated based on command-line arguments
SERVER_ADDRESS = ("0.0.0.0", 5000)
BUFFER_SIZE = 1024

# Define command prefixes
CMD_MKDIR = "mkdir"
CMD_SYNC = "sync"

# Create the UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Update server address to use the parsed arguments
server_socket.bind(SERVER_ADDRESS)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a UDP server for mkdir and sync commands.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address to bind the server (default: local machine).")
    parser.add_argument("--port", type=int, default=5000, help="Port number to bind the server.")

    args = parser.parse_args()

    SERVER_ADDRESS = (args.host, args.port)
    print(f"UDP server is listening on {SERVER_ADDRESS}...")

while True:
    try:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        command = data.decode('utf-8')
        print(f"Received command: {command} from {client_address}")

        if command.startswith(CMD_MKDIR):
            # Parse the directory name
            _, dir_path = command.split(' ', 1)
            try:
                os.makedirs(dir_path, exist_ok=True)
                response = "1"
            except Exception as e:
                response = "-1"

        elif command.startswith(CMD_SYNC):
            # Parse source and destination directories
            try:
                _, src_dir, dest_dir = command.split(' ', 2)
                if not os.path.exists(src_dir):
                    response = "-1"
                elif not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
                    response = "OK"
                else:
                    shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
                    response = "1"
            except Exception as e:
                response = "-1"

        else:
            response = "Unknown command. Use 'mkdir <dir_path>' or 'sync <src_dir> <dest_dir>'."

        # Send the response back to the client
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Response sent to {client_address}: {response}")

    except KeyboardInterrupt:
        print("Server shutting down.")
        break
    except Exception as e:
        print(f"Error: {e}")

# Close the socket
server_socket.close()
