import socket
import time
from header import pack_header, calculate_checksum

def send_message(message,sock, ack_num, seq_num):
    try:
        payload = message.encode('utf-8') 
        checksum = calculate_checksum(payload) 
        header = pack_header(seq_num, ack_num, 0b00000001, checksum, len(payload))  #pack_header(seq_num, ack_num, flags, checksum, payload_len)
        max_payload_size = 1024  # Tamanho máximo que seu servidor pode lidar por pacote
        if len(payload) > max_payload_size:
            return b'payload_error'
        
        packet = header + payload 
        sock.sendall(packet) 
        response = sock.recv(1024)  # Recebe a resposta do servidor
        return response
    except socket.timeout:
        print(f"\nTimeout: O servidor não respondeu a tempo. (seq_num: {seq_num})\n")
        return None


def create_client(host=socket.gethostname(), port=12345, timeout = 5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.settimeout(timeout)
        try:
            seq_num = 100
            
            while True:
                menu_input = input("Escolha uma opção:\n1 - para enviar uma mensagem íntegra\n"
                                   "2 - para simular e paralelismo\n3 - para simular o timeout no cliente\n"
                                   "4 - para enviar um pacote não integro\n0 - para encerrar o cliente"
                                   "\nDigite sua opção: ")
                if menu_input.lower() == '0':
                    break
                if menu_input.lower() == '1':
                    message = input("Digite sua mensagem: ")
                    ack_num = 1 
                    response = send_message(message, sock, ack_num, seq_num)

                    if response == b'ACK1':
                        time.sleep(4)
                        print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                        sock.sendall("ACK1c".encode())
                        time.sleep(2)
                        print(f"ACK1c sent to server. (seq_num: {seq_num})\n")
                    elif response == b'payload_error':
                        print("Message exceeds pay load. Packet dumped, sent a shorter message.")

                if menu_input.lower() == '2':
                    ack_num = 2
                    message = input("Digite sua mensagem: ")
                    response = send_message(message, sock, ack_num, seq_num)

                if menu_input.lower() == '3':
                    ack_num = 3
                    message = input("Digite sua mensagem: ")
                    response = send_message(message, sock, ack_num, seq_num)
                    
                    
                    print(f"No response from server, resending message. (seq_num: {seq_num})\n")
                    ack_num = 1
                    response = send_message(message, sock, ack_num, seq_num)

                    if response == b'ACK1':
                        time.sleep(4)
                        print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                        sock.sendall("ACK1c".encode())
                        time.sleep(2)
                        print(f"ACK1c sent to server. (seq_num: {seq_num})\n")

                if menu_input.lower() == '4':
                    ack_num = 4 
                    message = input("Digite sua mensagem: ")
                    response = send_message(message, sock, ack_num, seq_num)
                    
                    if response == b'ACK1':
                        time.sleep(4)
                        print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                        sock.sendall("ACK1c".encode())
                        time.sleep(2)
                        print(f"ACK1c sent to server. (seq_num: {seq_num})\n")
                    elif response == b'ACK4':
                        time.sleep(5)
                        print(f"ACK4 received from server. Packet compromised, sent it again. (seq_num: {seq_num})\n")
                        ack_num = 1 
                        response = send_message(message, sock, ack_num, seq_num)
                        print(f"Packet sent again. (seq_num: {seq_num})")
                        time.sleep(2)
                        if response == b'ACK1':
                            time.sleep(4)
                            print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                            sock.sendall("ACK1c".encode())
                            time.sleep(2)
                            print(f"ACK1c sent to server. (seq_num: {seq_num})\n")

                    else:
                        print(f"No ACK, resending. (seq_num: {seq_num})\n")
                
                seq_num += 1
                time.sleep(4)
        finally:
            print("Closing connection")
            sock.close()

if __name__ == '__main__':
    create_client()
