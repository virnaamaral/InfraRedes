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
            client_socket.settimeout(120)  # Timeout para recv()
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
            flag_timeout_client = 0
            header_data = client_socket.recv(header_size)
            if not header_data:
                print("No header received, closing connection...\n")
                break
            
            seq_num, ack_num, flags, checksum, payload_len = unpack_header(header_data)

            payload = client_socket.recv(payload_len)
            if not payload:
                print("No payload received, closing connection...\n")
                break

            received_checksum = calculate_checksum(payload)

            if ack_num == 3:
                flag_timeout_client = 1
                print("Sleeping for timeout...\n")
                time.sleep(6)
                
            if ack_num == 1:
                flag_timeout_client = 0

            if ack_num == 4:
                flag_timeout_client = 0
                checksum = checksum + 1

            if flag_timeout_client == 0:
                if checksum != received_checksum:
                    time.sleep(2)
                    print(f"Checksum error, corrupt package! (seq_num: {seq_num})\n")
                    client_socket.sendall(b'ACK4')
                    time.sleep(2)
                    print(f"ACK4 sent to cliente! Packet compromised! (seq_num: {seq_num})\n")
                    continue

                #time.sleep(2)
                data = payload.decode('utf-8')
                print(f"Received data: {data} (seq_num: {seq_num})\n")
                client_socket.sendall(b'ACK1')
                time.sleep(2)
                print(f"ACK1 sent to client! Data recieved with sucess! (seq_num: {seq_num})\n")
                
                ack_from_client = client_socket.recv(1024)
                
                if ack_from_client.decode('utf-8') == 'ACK1c':
                    time.sleep(4)
                    print(f"ACK1c received from client, proceeding to the next packet. (seq_num: {seq_num})\n")
                else:
                    print(f"Unexpected response or no ACK1 received send it again. (seq_num: {seq_num})\n")
                    ack_from_client = client_socket.recv(1024)  # Aguarda novamente pelo ACK1c
                    if ack_from_client.decode('utf-8') == 'ACK1c':
                        time.sleep(4)
                        print(f"ACK1c received from client, proceeding to the next packet. (seq_num: {seq_num})\n")
                    else:
                        print(f"No ACK1c received, closing connection. (seq_num: {seq_num})\n")
                        break
    except socket.timeout:
        print("\nClient inactive, closing connection.")
    finally:
        print("\nClosing client connection")
        client_socket.close()
        print("\nSocket closed.")

def create_server(host=socket.gethostname(), port=12345, timeout=120):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.settimeout(timeout)  # Timeout para accept()
    
    listener_thread = threading.Thread(target=server_listen, args=(server_socket,))
    listener_thread.start()
    listener_thread.join()

if __name__ == '__main__':
    create_server()
