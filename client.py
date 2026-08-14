import argparse
import socket
import threading
from crypto_utils import decrypt, encrypt, validate_mono_key, only_letters_key


def choose_mode():
    print('Escolha o modo de transmissão:')
    print('1 - Sem criptografia')
    print('2 - Cifra de César')
    print('3 - Cifra monoalfabética')
    print('4 - Cifra de Playfair')
    print('5 - Cifra de Vigenère')
    while True:
        mode = int(input('Opção: '))
        if mode in range(1, 6):
            break
        print('Opção inválida.')
    key = ''
    if mode == 2:
        while True:
            key = input('Chave inteira (0 a 25): ')
            if key.isdigit() and 0 <= int(key) <= 25:
                break
            print('Chave inválida.')
    elif mode == 3:
        while True:
            key = input('Chave com 26 letras sem repetição: ')
            try:
                key = validate_mono_key(key)
                break
            except ValueError as exc:
                print(exc)
    elif mode in (4, 5):
        while True:
            key = input('Palavra-chave somente com letras: ')
            try:
                key = only_letters_key(key)
                break
            except ValueError as exc:
                print(exc)
    return mode, key


def receive_loop(sock_file, mode, key):
    while True:
        line = sock_file.readline()
        if not line:
            print('\n[conexão encerrada pelo servidor]')
            break
        cipher = line.rstrip('\n')
        print(f'\nMensagem cifrada recebida: {cipher}')
        print(f'Mensagem decifrada: {decrypt(mode, cipher, key)}')
        print('Mensagem> ', end='', flush=True)


def main():
    parser = argparse.ArgumentParser(description='Cliente TCP do chat criptografado')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    mode, key = choose_mode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((args.host, args.port))
        sock.sendall((f'{mode}|{key}' + '\n').encode('utf-8'))
        sock_file = sock.makefile('r', encoding='utf-8')
        threading.Thread(target=receive_loop, args=(sock_file, mode, key), daemon=True).start()
        while True:
            msg = input('Mensagem> ')
            cipher = encrypt(mode, msg, key)
            print(f'Mensagem cifrada transmitida: {cipher}')
            sock.sendall((cipher + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()
