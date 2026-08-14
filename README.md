# Projeto 1 - Parte 1: Chat TCP com Criptografia Simétrica

Implementação em Python de um chat em modo texto usando sockets TCP. O cliente escolhe a cifra no início da conexão e envia ao servidor a opção e a chave, que passam a valer nos dois sentidos da conversa durante a sessão.

## Arquivos

- `server.py`: servidor TCP com porta configurável.
- `client.py`: cliente TCP com menu de escolha da cifra.
- `crypto_utils.py`: implementação das cifras e normalização de texto.
- `test_crypto_utils.py`: testes automatizados das cifras.

## Como executar

Abra dois terminais.

Terminal 1:

```bash
python3 server.py --port 5000
```

Terminal 2:

```bash
python3 client.py --host 127.0.0.1 --port 5000
```

Depois escolha uma das opções:

1. Sem criptografia
2. Cifra de César
3. Cifra monoalfabética
4. Cifra de Playfair
5. Cifra de Vigenère

## Regras atendidas

- Comunicação TCP entre cliente e servidor.
- Execução em consoles separados.
- Conversa bidirecional com `threading`, permitindo receber mensagens sem esperar o outro lado encerrar a digitação.
- Exibição da mensagem cifrada recebida e da mensagem decifrada.
- Exibição da mensagem cifrada transmitida, útil para capturar no Wireshark.
- Porta configurável no servidor por `--port`.
- Um cliente por vez, conforme permitido na primeira parte do projeto.

## Tratamento de texto

Para César, monoalfabética e Vigenère:

- letras são convertidas para maiúsculas;
- acentos são removidos;
- `Ç` é tratado como `C`;
- espaços, números e pontuação permanecem inalterados;
- na Vigenère, a chave avança somente quando uma letra é processada.

Para Playfair:

- a chave é normalizada para maiúsculas;
- acentos, espaços e símbolos são removidos;
- `J` é convertido para `I`;
- a matriz 5x5 usa `I/J` na mesma posição;
- letras repetidas no mesmo par recebem `X` entre elas;
- se sobrar uma letra sem par, é acrescentado `X` ao final.

## Testes

```bash
python3 -m unittest -v
```
