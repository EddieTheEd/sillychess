import socket

def main():
    default_host = '127.0.0.1' # local host for testing
    default_port = 12345

    host = input(f"Enter server IP address (default: {default_host}): ") or default_host
    port = int(input(f"Enter server port (default: {default_port}): ") or default_port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server.")

    while True:
        message = input("Enter message: ")
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")

    client_socket.close()

if __name__ == "__main__":
    main()
