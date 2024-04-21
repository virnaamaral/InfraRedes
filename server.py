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
        raw_buffer= b""
        while True:
            flag_timeout_client = 0
            data = client_socket.recv(1024)

            if not data:
                print("No data received, closing connection...\n")
                break
            
            raw_buffer += data
            buffer = b""
            packet_count = 0
            window_len = 5
            flag_batch = 0

            while b'\n' in raw_buffer:
                # Extrai um pacote delimitado pelo '\n'
                raw_packet, raw_buffer = raw_buffer.split(b'\n', 1)
                packet_count += 1  # Incrementa o contador de pacotes
                buffer += raw_packet #cria um array dos pacotes crus sem o \n
 
            '''if packet_count > window_len: #se qtd pacotes for maior que a janela
                if window_len >1: # e janela for maior que 1
                    window_len -= 1 # diminui 1
            else: # se qtd pacotes
                window_len += 1  '''


            while True:
                if not buffer:  # Verifica se o buffer está vazio
                    print("Empty Buffer, no message do process. Type next Message.\n")
                    break 

                if len(buffer) < header_size:
                    print("Header compromised. Packet discarted, Type next Message\n")
                    break

                header_data = buffer[:header_size] #pega primeira parte do cabeçalho

                seq_num, ack_num, flags, checksum, payload_len = unpack_header(header_data)

                total_packet_size = header_size + payload_len
                if len(buffer) < total_packet_size:
                    print ("payload completo nao foi recebido")
                    break

                payload = buffer[header_size:total_packet_size] #faz o slice da mensagem

                received_checksum = calculate_checksum(payload)

                if ack_num == 3:
                    flag_timeout_client = 1
                    print("Sleeping for timeout...\n")
                    time.sleep(11)

                if ack_num == 2: 
                    flag_timeout_client = 1
                    flag_batch = 1
                    if checksum != received_checksum:
                        time.sleep(2)
                        print(f"Checksum error, corrupt package! (seq_num: {seq_num})\n")
                        client_socket.sendall(b'ACK4')
                        time.sleep(2)
                        print(f"ACK4 sent to cliente! Packet compromised! (seq_num: {seq_num})\n")
                        continue
                    data = payload.decode('utf-8')
                    print(f"Received data: {data} (seq_num: {seq_num})\n")
                    #break
                    
                    
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
                        break

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
                    

                buffer = buffer[total_packet_size:]

            if flag_batch == 1:
                    client_socket.sendall(b'ACKALL')
                    time.sleep(2)
                    print(f"ACKALL sent to client! Data recieved with sucess! (seq_num: {seq_num})\n")
                    
                    ack_from_client = client_socket.recv(1024)
                    
                    if ack_from_client.decode('utf-8') == 'ACKALLc':
                        time.sleep(4)
                        print(f"ACKALLc received from client, proceeding to the next packet. (seq_num: {seq_num})\n")
                    else:
                        print(f"Unexpected response or no ACKALL received send it again. (seq_num: {seq_num})\n")
                        ack_from_client = client_socket.recv(1024)  # Aguarda novamente pelo ACK1c
                        if ack_from_client.decode('utf-8') == 'ACKALLc':
                            time.sleep(4)
                            print(f"ACKALLc received from client, proceeding to the next packet. (seq_num: {seq_num})\n")
                        else:
                            print(f"No ACKALLc received, closing connection. (seq_num: {seq_num})\n")
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
