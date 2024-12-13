import socket

SERVER_ADDRESS = ('127.0.0.1', 5000)

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(command.encode('utf-8'), SERVER_ADDRESS)
        response, _ = client_socket.recvfrom(1024)
        result = response.decode('utf-8')
        if result == "1":
            print("Command succeeded.")
        elif result == "-1":
            print("Command failed.")
        else:
            print("Unexpected server response:", result)

# Example: Create a directory
send_command("mkdir C:/Temp/abc")

# Example: Synchronize directories
send_command("sync C:/Temp/abc C:/Temp/abc2")
