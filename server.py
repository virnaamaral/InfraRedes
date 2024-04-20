import socket
import threading
import time
from header import unpack_header, header_size, calculate_checksum

def server_listen(server_socket):
    server_socket.listen(5)
    print("Server listening for connections...\n")
    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}\n")
            client_socket.settimeout(45)  # Timeout para recv()
            handle_client(client_socket)
        except socket.timeout:
            print("No connections within the timeout period.\n")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def handle_client(client_socket):
    try:
        while True:
            header_data = client_socket.recv(header_size)
            if not header_data:
                print("No header received, closing connection...\n")
                break
            
            seq_num, ack_num, flags, checksum, payload_len = unpack_header(header_data)
            

            if payload_len > 1024:
                print("Error: Payload too large\n")
                client_socket.sendall(b'Error: Payload too large\n')
                continue

            payload = client_socket.recv(payload_len)
            if not payload:
                print("No payload received, closing connection...\n")
                break

            received_checksum = calculate_checksum(payload)
            
            if ack_num == 4:
                checksum = checksum + 1

            if checksum != received_checksum:
                time.sleep(2)
                print(f"Checksum error, corrupt package! (seq_num: {seq_num})\n")
                client_socket.sendall(b'ACK4')
                time.sleep(2)
                print(f"ACK4 sent to cliente! Packet compromised! (seq_num: {seq_num})\n")
                
                continue

            time.sleep(6)
            data = payload.decode('utf-8')
            print(f"Received data: {data} (seq_num: {seq_num})\n")
            client_socket.sendall(b'ACK1')
            time.sleep(2)
            print(f"ACK1 sent to client! Data recieved with sucess! (seq_num: {seq_num})\n")
            
            ack_from_client = client_socket.recv(1024)
            
            if ack_from_client.decode() == "ACK1c":
                time.sleep(4)
                print(f"ACK1c received from client, proceeding to the next packet. (seq_num: {seq_num})\n")

            else:
                print(f"Unexpected response or no ACK1 received send it again. (seq_num: {seq_num})\n")

    except socket.timeout:
        print("Client inactive, closing connection.")
    finally:
        client_socket.close()
        print("Socket closed.")

def create_server(host=socket.gethostname(), port=12345, timeout=45):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.settimeout(timeout)  # Timeout para accept()
    
    listener_thread = threading.Thread(target=server_listen, args=(server_socket,))
    listener_thread.start()
    listener_thread.join()

if __name__ == '__main__':
    create_server()
