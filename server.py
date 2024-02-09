import socket
import threading

def read_data(address, data):
    print(f"Received from {address}: {data}")

def handle_client(client_socket, addr):
    print(f"Accepted connection from {addr}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        
        read_data(addr, data.decode())
        client_socket.sendall(data)
    print(f"Connection from {addr} closed")
    client_socket.close()

def get_internal_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to a remote server (doesn't matter which one)
        s.connect(("8.8.8.8", 80))

        # Get the socket's own IP address (this is the internal IP address)
        internal_ip = s.getsockname()[0]

        return internal_ip
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def main():
    default_host = '0.0.0.0'
    default_port = 12345

    internal_ip = get_internal_ip()
    if internal_ip:
        print(f"Internal IP address of the server: {internal_ip}")
    else:
        print("Failed to retrieve internal IP address.")

    host = input(f"Enter server IP address (default: {default_host}): ") or default_host
    port = int(input(f"Enter server port (default: {default_port}): ") or default_port)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
