# Projeto Infraestrutura de Comunicação
Projeto desenvolvido para a disciplina de Infraestrutura de Comunicação, na graduação em Ciência da Computação na [CESAR School](https://www.cesar.school)

## O que é?

Uma aplicação Cliente-Servidor que, na camada de Aplicação, fornece um transporte confiável de dados, considerando um canal com perdas de dados e erros.

## Como funciona?
- O Cliente se conecta ao Servidor através do localhost (quando na mesma máquina) ou via IP, esta comunicação ocorrendo via sockets.

- O programa abarca o envio de pacotes da camada de aplicação de forma Isolada, a partir do Cliente, ou em Lotes, com destino ao Servidor, que pode confirmar a recepção de forma individual ou a recepção em Grupo dessas mensagens (aceita ambas as configurações)

- Eventuais falhas de integridade e/ou perdas de mensagens são simuladas a nível de Aplicação, sendo possível a inserção de ‘erros’ no lado Cliente, verificáveis pelo Servidor

> Esta comunicação apresenta todas as características do transporte
confiável de dados, descritas abaixo em [Funcionalidades](#funcionalidades)

> Confira nosso protocolo de aplicação proposto, com as requisições e respostas descritas, acessível abaixo em [Protocolo de Aplicação](#protocolo-de-aplicação)

## Funcionalidades

- Soma de verificação
- Temporizador
- Número de sequência
- Reconhecimento

- Em Construção...
  - Reconhecimento negativo
  - Janela, paralelismo
  - Método de checagem de integridade

## Protocolo de Aplicação

## 🤓 Como Usar?


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
<br></br>
