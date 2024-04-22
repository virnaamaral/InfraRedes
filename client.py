import socket
import time
from header import pack_header, calculate_checksum

def send_message(message, sock, ack_num, seq_num):
    try:
        payload = message.encode('utf-8') 
        checksum = calculate_checksum(payload) 
        header = pack_header(seq_num, ack_num, 0b00000001, checksum, len(payload))  #pack_header(seq_num, ack_num, flags, checksum, payload_len)
        max_payload_size = 1024  # Tamanho máximo que seu servidor pode lidar por pacote
        if len(payload) > max_payload_size:
            return b'payload_error'
        packet = header + payload + b'\n'
        sock.sendall(packet)
        print(f"\nSent packet. (seq_num: {seq_num})")
        response = sock.recv(1024)  # Recebe a resposta do servidor
        return response
    except socket.timeout:
        print(f"\nTimeout: Server did not respond. (seq_num: {seq_num})\n")
        return None

def create_message(message, sock, ack_num, seq_num):
    payload = message.encode('utf-8') 
    checksum = calculate_checksum(payload) 
    header = pack_header(seq_num, ack_num, 0b00000001, checksum, len(payload))  #pack_header(seq_num, ack_num, flags, checksum, payload_len)
    max_payload_size = 1024  # Tamanho máximo que seu servidor pode lidar por pacote
    if len(payload) > max_payload_size:
        return b'payload_error'
    packet = header + payload 
    return packet

def send_batch(messages, sock, ack_num, seq_start):
    batch_packets = b'' # inicializa como byte, como array n vai dar certo 
    seq_num = seq_start
    for message in messages:
        packet = create_message(message, sock, ack_num, seq_num) #cria os packets de todas as mensagens
        if packet == b'payload_error':
            return b'payload_error'
        batch_packets += packet + b'\n' #da join aqui em todos os packets e os separa por \n
        seq_num += 1
        time.sleep(2)  # Aguarda um pouco entre as mensagens para simular paralelismo
    sock.sendall(batch_packets)
    print(f"\nSent batch packet")
    response = sock.recv(1024)
    return response

def send_batch_response_per_packet(messages, sock, ack_num, seq_start,window_size):
    seq_num = seq_start
    total_messages = len(messages)
    index = 0

    print(f'\nTamanho da janela: {window_size}\n')
    
    while index < total_messages: 
        window_end = min(index + window_size, total_messages)
        batch_packets = b'' # inicializa como byte, como array n vai dar certo 

        print(f'Início da Janela Enviando mensagens {index + 1} a {window_end}')

        for i in range(index, window_end):
            packet = create_message(messages[i], sock, ack_num, seq_num) #cria os packets de todas as mensagens
            if packet == b'payload_error':
                return b'payload_error'
            batch_packets += packet + b'\n' #da join aqui em todos os packets e os separa por \n
            seq_num += 1
            #time.sleep(2)  # Aguarda um pouco entre as mensagens para simular paralelismo
        
        sock.sendall(batch_packets)
        print(f"\nSent batch packet {seq_num - (window_end - index)} to {seq_num - 1}\n\n")

        current_seq = seq_num - (window_end - index)
        for _ in range (index, window_end):
            response = sock.recv(1024)
            if response == b'ACK1':
                time.sleep(4)
                print(f"ACK1 received from server! Message received successfuly! (seq_num: {current_seq})\n")
                sock.sendall("ACK1c".encode())
                time.sleep(2)
                print(f"ACK1c sent to server. (seq_num: {current_seq})\n")
            elif response == b'payload_error':
                print("Message exceeds pay load. Packet dumped, sent a shorter message.")
            current_seq += 1 

        print(f'Fim da Janela')
        
        index += window_size
    
                        

def create_client(host=socket.gethostname(), port=12345, timeout = 13):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.settimeout(timeout)
        try:
            seq_num = 100
            window_size = 3

            while True:
                            
                num_messages=0
                menu_input = input("\nEscolha uma opção:\n1 - para enviar uma mensagem íntegra\n"
                                   "2 - para simular e paralelismo\n3 - para simular o timeout no cliente\n"
                                   "4 - para enviar um pacote não integro\n0 - para encerrar o cliente"
                                   "\nDigite sua opção: ")
                
                if menu_input.lower() == '0':
                    break
                
                if menu_input.lower() == '1':
                    message = input("\nDigite sua mensagem: ")
                    ack_num = 1 
                    response = send_message(message, sock, ack_num, seq_num)

                    if response == b'ACK1':
                        time.sleep(4)
                        print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                        sock.sendall("ACK1c".encode())
                        time.sleep(2)
                        print(f"ACK1c sent to server. (seq_num: {seq_num})\n")
                    elif response == b'payload_error':
                        print("\nMessage exceeds pay load. Packet dumped, sent a shorter message.\n")

                if menu_input.lower() == '2':
                    response_type = input("\nInforme como deseja receber a resposta:\n1 - Resposta por cada mensagem enviada\n2 - Unica resposta pelo batch\nDigite sua opção: ")
                    
                    if response_type == '1':
                        ack_num = 1 #novo  pra simular 1 resposta por mensagem
                        num_messages = int(input("\nDigite o número de mensagens a enviar: \n"))
                        messages = [input(f"\nDigite a mensagem {i + 1}: ") for i in range(num_messages)]
                        response = send_batch_response_per_packet(messages, sock, ack_num, seq_num, window_size)

                        if response == b'payload_error':
                            print("Message exceeds pay load. Packet dumped, sent a shorter message.\n")
                            
                    else:
                        ack_num = 2 #ack_para receber em uma response só. 
                        num_messages = int(input("Digite o número de mensagens a enviar: "))
                        messages = [input(f"Digite a mensagem {i + 1}: ") for i in range(num_messages)]
                        response = send_batch(messages, sock, ack_num, seq_num)

                    if response == b'ACK1':
                        time.sleep(4)
                        print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                        sock.sendall("ACK1c".encode())
                        time.sleep(2)
                        print(f"ACK1c sent to server. (seq_num: {seq_num})\n")
                    elif response == b'ACKALL':
                        time.sleep(4)
                        print(f"\nACKALLc received from server! Message received successfuly!\n")
                        sock.sendall("ACKALLc".encode())
                        time.sleep(2)
                        print(f"ACKALLc sent to server.\n")

                    elif response == b'payload_error':
                        print("\nMessage exceeds pay load. Packet dumped, sent a shorter message.")
                        
                    
                    

                    #vc recever confirmação por mensagem ou por grupo?
                    # while para receber mesnagem
                    #message[]
                    #msg_len = len(messagem)
                    
                    # message = input("Digite sua mensagem: ")
                    # response = send_message(message, sock, ack_num, seq_num)

                if menu_input.lower() == '3':
                    ack_num = 3
                    message = input("\nDigite sua mensagem: ")
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
                    message = input("\nDigite sua mensagem: ")
                    response = send_message(message, sock, ack_num, seq_num)
                    
                    if response == b'ACK1':
                        time.sleep(4)
                        print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                        sock.sendall("ACK1c".encode())
                        time.sleep(2)
                        print(f"\nACK1c sent to server. (seq_num: {seq_num})\n")
                    elif response == b'ACK4':
                        time.sleep(5)
                        print(f"\nACK4 received from server. Packet compromised, sent it again. (seq_num: {seq_num})\n")
                        ack_num = 1 
                        response = send_message(message, sock, ack_num, seq_num)
                        print(f"\nPacket sent again. (seq_num: {seq_num})")
                        time.sleep(2)
                        if response == b'ACK1':
                            time.sleep(4)
                            print(f"\nACK1 received from server! Message received successfuly! (seq_num: {seq_num})\n")
                            sock.sendall("ACK1c".encode())
                            time.sleep(2)
                            print(f"\nACK1c sent to server. (seq_num: {seq_num})\n")
                    elif response == b'payload_error':
                        print("\nMessage exceeds pay load. Packet dumped, sent a shorter message.")

                    else:
                        print(f"\nNo ACK, resending. (seq_num: {seq_num})\n")
                
                if num_messages == 0:
                    seq_num += 1
                else:
                    seq_num = seq_num + num_messages
                
                #print(f"proximo numero de sequencia é {seq_num} \n")
                
                time.sleep(4)
        finally:
            print("\nClosing connection")
            sock.close()

if __name__ == '__main__':
    create_client()
