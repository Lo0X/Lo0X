import argparse
import socket
import threading
from crypto_utils import decrypt, encrypt


def receive_loop(sock_file, mode, key):
    while True:
        line = sock_file.readline()
        if not line:
            print('\n[conexão encerrada pelo cliente]')
            break
        cipher = line.rstrip('\n')
        print(f'\nMensagem cifrada recebida: {cipher}')
        print(f'Mensagem decifrada: {decrypt(mode, cipher, key)}')
        print('Resposta> ', end='', flush=True)


def main():
    parser = argparse.ArgumentParser(description='Servidor TCP do chat criptografado')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((args.host, args.port))
        srv.listen(1)
        print(f'Servidor aguardando conexão em {args.host}:{args.port}...')
        conn, addr = srv.accept()
        with conn:
            sock_file = conn.makefile('r', encoding='utf-8')
            header = sock_file.readline().rstrip('\n').split('|', 1)
            mode = int(header[0])
            key = header[1] if len(header) > 1 else ''
            print(f'Cliente conectado: {addr}. Modo: {mode}.')
            threading.Thread(target=receive_loop, args=(sock_file, mode, key), daemon=True).start()
            while True:
                msg = input('Resposta> ')
                cipher = encrypt(mode, msg, key)
                print(f'Mensagem cifrada transmitida: {cipher}')
                conn.sendall((cipher + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()
