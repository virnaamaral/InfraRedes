# Projeto Infraestrutura de Comunicação
Projeto desenvolvido para a disciplina de Infraestrutura de Comunicação, na graduação em Ciência da Computação na [CESAR School](https://www.cesar.school)

## 💻 Grupo 4:
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/anabxalves">
        <img src="https://avatars.githubusercontent.com/u/108446826?v=4" width="100px;" alt="Foto Ana"/><br>
        <sub>
          <b>Ana Beatriz Alves</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Caiobadv">
        <img src="https://avatars.githubusercontent.com/u/117755420?v=4" width="100px;" alt="Foto Caio"/><br>
        <sub>
          <b>Caio Barreto</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Criismnaga">
        <img src="https://avatars.githubusercontent.com/u/104402971?v=4" width="100px;" alt="Foto Cris"/><br>
        <sub>
          <b>Cristina Matsunaga</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/DaviMauricio">
        <img src="https://avatars.githubusercontent.com/u/71526685?v=4" width="100px;" alt="Foto Davi"/><br>
        <sub>
          <b>Davi Maurício</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/FernandaFBMarques">
        <img src="https://avatars.githubusercontent.com/u/101741395?v=4" width="100px;" alt="Foto Nanda"/><br>
        <sub>
          <b>Maria Fernanda Marques</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/virnaamaral">
        <img src="https://avatars.githubusercontent.com/u/116957619?v=4" width="100px;" alt="Foto Virnas"/><br>
        <sub>
          <b>Virna Amaral</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
<br>

## 🧐 O que é?

Uma aplicação Cliente-Servidor que, na camada de Aplicação, fornece um transporte confiável de dados, considerando um canal com perdas de dados e erros.

## 💡 Como funciona?
- O Cliente se conecta ao Servidor através do localhost (quando na mesma máquina) ou via IP, esta comunicação ocorrendo via sockets.

- O programa abarca o envio de pacotes da camada de aplicação de forma Isolada, a partir do Cliente, ou em Lotes, com destino ao Servidor, que pode confirmar a recepção de forma individual ou a recepção em Grupo dessas mensagens (aceita ambas as configurações)

- Eventuais falhas de integridade e/ou perdas de mensagens são simuladas a nível de Aplicação, sendo possível a inserção de ‘erros’ no lado Cliente, verificáveis pelo Servidor

> Esta comunicação apresenta todas as características do transporte
confiável de dados, descritas abaixo em [Funcionalidades](#funcionalidades)

> Confira nosso protocolo de aplicação proposto, com as requisições e respostas descritas, acessível abaixo em [Protocolo de Aplicação](#protocolo-de-aplicação)

## 🤓 Como Usar?

1. **Instalação do Python**:
    > Certifique-se de ter o Python instalado em seu sistema.

2. **Execução do Servidor**:
    > Em um terminal ou prompt de comando, navegue até o diretório onde você salvou o arquivo `server.py`, e execute o servidor digitando:
    >- Windows/Linux: `python server.py`
    >- MacOs: `python3 server.py`

3. **Execução do Cliente**:
    > Em outro terminal ou prompt de comando (ou uma nova janela no mesmo terminal), navegue até o diretório onde você salvou o arquivo `client.py`, e execute o cliente digitando:
    >- Windows/Linux: `python client.py`
    >- MacOs: `python3 client.py`

4. **Interagindo com o Cliente**:
    > No menu do Cliente, serão ofertados várias opções, como enviar mensagens ou simular falhas
    > Você pode escolher enviar mensagens íntegras, simular pacotes perdidos, simular timeout no cliente, enviar pacotes não íntegros, ou encerrar o Cliente

5. **Observando a Comunicação**:
    > Enquanto o Cliente e o Servidor estiverem em execução, o terminal do Servidor mostrará as mensagens de comunicação e os logs de eventos.
    >- O servidor estará aguardando conexões e processando as mensagens recebidas do cliente
    >- O cliente enviará mensagens de acordo com suas escolhas no menu

6. **Encerrando a Execução**:
    > O Cliente será encerrado ao digitar *0* no menu, e ao esperarmos 45 segundos, o Servidor também é encerrado se não houver novas conexões de Clientes durante esse período.
    >- Atendendo a essas duas condições, ambos, Servidor e Cliente, serão encerrados, e mensagens indicando o fechamento da conexão serão mostradas nos respectivos terminais

## Funcionalidades

- **Soma de verificação**: É o método usado para verificar a integridade dos dados transmitidos em uma rede.
  > Envolve somar todos os bytes de dados em um pacote e calcular um valor de verificação, que é enviado junto com os dados, sendo recalculado pelo destinatário para verificar se os dados foram corrompidos durante a transmissão

- **Temporizador**: É o mecanismo usado para controlar o tempo de espera por uma resposta.
  >- Quando um dispositivo envia dados, é definido um temporizador para aguardar uma resposta dentro de um determinado período
  >- Se a resposta não for recebida dentro desse tempo, o temporizador expira e o dispositivo retransmite os dados

- **Número de sequência**: É uma sequência de números usados para identificar e ordenar mensagens transmitidas em uma rede.
  > Cada mensagem é atribuída a um número de sequência único, que é usado pelo receptor para reconstruir a ordem das mensagens e detectar a perda ou duplicação de mensagens

- **Reconhecimento**: É o mecanismo usado para confirmar a recepção de dados.
    > Quando um dispositivo recebe dados, ele envia de volta um reconhecimento (ACK) para informar ao remetente que os dados foram recebidos com sucesso, ajudando no controle de fluxo e na garantia de entrega de dados.

- **Reconhecimento negativo**: É o tipo de resposta enviada pelo destinatário para indicar que houve um problema na recepção dos dados.

- **Janela e paralelismo**: Usado para limitar o número de pacotes que podem ser enviados sem aguardar um reconhecimento, o que permite um certo paralelismo na transmissão de dados, fazendo com que o remetente envie vários pacotes antes de receber um reconhecimento.

- _**Método de checagem de integridade**_: Métodos usados para garantir que os dados transmitidos não tenham sido corrompidos ou alterados durante a transmissão.

## Protocolo de Aplicação

Aqui definimos e explicamos o desenvolvimento das regras e procedimentos que o Cliente e o Servidor seguirão para comunicar-se efetivamente, garantindo um transporte confiável de dados sobre uma rede que pode estar sujeita a perdas de dados e erros.

Abaixo, temos cada elemento que deve ser considerado segundo o protocolo desenvolvido:

1. **Conexão e Endereçamento**: O Cliente se conecta ao Servidor utilizando o host local `socket.gethostname()` e a porta 12345 por padrão, conforme especificado nos códigos `create_server()` e `create_client()`. Isso significa que a comunicação ocorre na mesma máquina, a menos que você especifique um IP diferente para o *host*.
Porém, o `socket.gethostname()` faz com que, de forma automática, a porta do Servidor seja uma aleatória da máquina, esperarando por conexões (`server_socket.bind((host, port))`).

    - Parâmetros e Valores Default:
      - `host = socket.gethostname()`:
        > *host* é um parâmetro que especifica o endereço IP ou o nome do *host* em que o Servidor deve operar

        > `socket.gethostname()` retorna o nome do *host* no qual o Python está sendo executado, que é então resolvido para um endereço IP quando o *socket* é criado e vinculado, significando que o Servidor será acessível neste endereço de *host*
        
        > Esse valor padrão permite que a função seja chamada sem especificar explicitamente um host, fazendo com que o servidor opere na máquina local

      - `port = 12345`:
        > *port* é um parâmetro que especifica a porta TCP na qual o Servidor estará ouvindo
        
        > O número *12345* é um valor padrão para a porta se nenhum outro for especificado no momento da chamada da função

      - `timeout = 5`:
        > *timeout* é um parâmetro que define um limite de tempo (em segundos) que o servidor esperará por uma conexão antes de gerar uma exceção de *timeout* se nenhuma conexão for estabelecida

        > O valor *5* é o valor estipulado que indica que o cliente esperará por conexões durante 5 segundos antes de desistir temporariamente

2. **Formato das Mensagens**: O formato das mensagens inclui um cabeçalho definido pelo arquivo `header.py`. O cabeçalho possui os seguintes campos:
    - Número de sequência (*seq_num*): identifica a ordem das mensagens
    - Número de reconhecimento (*ack_num*): confirma o recebimento de mensagens
    - *flags*: utilizadas para controle de fluxo e detecção de erros
    - Soma de verificação (*checksum*): verifica a integridade dos dados
    - Comprimento do payload (*payload_len*): indica o tamanho dos dados enviados

      > Além do cabeçalho, as mensagens contêm dados de payload, como mensagens de texto digitadas pelo usuário

3. **Início e Término da Comunicação**: A comunicação é iniciada quando o Cliente se conecta ao Servidor usando `sock.connect((host, port))`, portanto a conexão estabelecida já inicia a comunicação. Já o término da comunicação pode ocorrer quando o usuário escolhe a opção *0* para encerrar o Cliente (`menu_input.lower() == '0'`)
    > A conexão é fechada quando o Cliente encerra

4. **Controle de Fluxo e Erro**:
    - *Soma de Verificação*: A soma de verificação é calculada utilizando a função `calculate_checksum(data)` no Cliente e verificada no Servidor, para garantir a integridade dos dados
    - *Temporizador*: São usados para gerenciar timeouts. O Servidor define um *timeout* para aceitar conexões `flag_timeout_client = 0` e o cliente, ao ser cirado, define um timeout limite para esperar antes de retransmitir, em caso de erros
    - *Número de Sequência e Reconhecimento*: Os números de sequência são atribuídos às mensagens para identificar sua ordem, sendo os reconhecimentos utilizados para confirmar o recebimento das mensagens pelo servidor, incluindo o envio de *ACK1* ou *ACK4* dependendo do estado da mensagem recebida
    - *Janela de Transmissão*: O Cliente pode enviar as mensagens que desejar, mas a janela limita a quantidade de mensagens que serão efetivamente enviadas ao servidor, ou seja, só será enviado mais mensagens se receber a confirmação do servidor para as mensagens anteriores. O tamanho da janela pode ser definido de diferentes formas, como por quantidade de bytes do buffer, mas no caso específico é limitado pela quantidade de mensagens. Isso significa que, se a janela estiver definida como 3 e o cliente enviar 5 mensagens, o sistema irá processar as 3 primeiras mensagens e só depois processará as outras duas, pois a janela permite o envio de até 3 mensagens de uma vez.


5. **Simulação de Falhas**: É feita através das opções no menu do Cliente.
    - A opção 4 simula um pacote não íntegro, feito deliberadamente para testar o comportamento do protocolo em situações de erro
    - Já a opção 3 simula o timeout do cliente, implementando um mecanismo para lidar com situações em que a resposta do Servidor demora mais do que o esperado, evitando que o Cliente fique indefinidamente esperando por uma resposta que pode não chegar.
      - No Cliente definiu-se um limite de tempo de *5 segundos* para esperar por uma resposta do Servidor
      - Se o Cliente não receber uma resposta dentro do tempo limite especificado, ele assume que houve uma falha na transmissão e retransmite a mensagem
        > Vale ressaltar que, durante a execução, o Cliente informa ao usuário sobre o status das mensagens enviadas e se houve algum timeout detectado
    - A falha de integridade é simulada alterando o *checksum* do pacote no servidor `if ack_num == 4: checksum = checksum + 1`

6. **Configuração do Servidor para Respostas**: O Servidor responde ao Cliente com mensagens de *ACK1* ou *ACK4* para confirmar o recebimento e integridade das mensagens, utilizadas pelo Cliente para determinar se a mensagem foi entregue com sucesso ou se precisa ser retransmitida.

## 🗂️ Explicando os Arquivos

### `server.py`
Responsável por implementar um servidor que fica ouvindo por conexões de clientes.

Utiliza a biblioteca *socket* para comunicação em rede, *threading* para lidar com múltiplas conexões simultaneamente e funções definidas no arquivo `header.py` para manipular o cabeçalho dos pacotes de dados.

- Funções do `server.py`

> `server_listen(server_socket)`: Responsável por aceitar conexões de clientes e iniciar a comunicação com cada cliente conectado

> `handle_client(client_socket)`: Onde a comunicação real com cada Cliente acontece, incluindo a recepção e envio de dados, verificação de checksum, tratamento de erros e controle de fluxo

> `create_server(host, port, timeout)`: Cria o socket do servidor, faz o bind com o endereço e porta especificados, e inicia a escuta por conexões utilizando uma thread.

### `client.py`
Implementa o Cliente que se conecta ao servidor para enviar e receber mensagens.

Utiliza a biblioteca *socket* para comunicação em rede, além das funções definidas no arquivo `header.py` para empacotar o cabeçalho dos pacotes de dados.

- Funções do `client.py`

> `send_message(message, sock, ack_num, seq_num)`: Empacota a mensagem junto com o cabeçalho, calcula o checksum, envia o pacote para o servidor e espera por uma resposta

> `create_client(host, port)`: Onde o cliente é criado, conectando-se ao servidor, e interagindo com o usuário para enviar mensagens ou simular diferentes cenários de comunicação (como pacotes perdidos ou timeout).

### `header.py`
Contém funções utilitárias para manipular o cabeçalho dos pacotes de dados.

Utiliza a biblioteca *struct* para empacotar e desempacotar os dados de acordo com um formato específico definido em *header_format*.

- Funções do `header.py`

> `calculate_checksum(data)`: Calcula o checksum dos dados passados como argumento.

> `pack_header(seq_num, ack_num, flags, checksum, payload_len)`: Empacota os campos do cabeçalho em um formato específico.

> `unpack_header(header_bytes)`: Desempacota os dados do cabeçalho a partir de bytes recebidos.
