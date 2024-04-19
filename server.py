import socket
import threading
import time
import header 

def server_listen(server_socket):
    server_socket.listen(5)
    print("Server listening for connections...")
    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")
            client_socket.settimeout(45)  # Timeout para recv()
            handle_client(client_socket)
        except socket.timeout:
            print("No connections within the timeout period.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            client_socket.sendall(b'ACK')
    except socket.timeout:
        print("Client inactive, closing connection.")
    finally:
        client_socket.close()
        print("Connection closed.")

def create_server(host=socket.gethostname(), port=12345, timeout=60):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.settimeout(timeout)  # Timeout para accept()
    
    listener_thread = threading.Thread(target=server_listen, args=(server_socket,))
    listener_thread.start()
    listener_thread.join()

if __name__ == '__main__':
    create_server()
