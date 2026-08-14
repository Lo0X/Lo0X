import string
import unicodedata

ALPHABET = string.ascii_uppercase


def normalize_char(ch: str) -> str:
    decomp = unicodedata.normalize('NFD', ch)
    base = ''.join(c for c in decomp if unicodedata.category(c) != 'Mn')
    return base.upper().replace('Ç', 'C')


def normalize_keep_nonletters(text: str) -> str:
    return ''.join(normalize_char(ch) if normalize_char(ch)[:1].isalpha() else ch for ch in text)


def only_letters_key(key: str) -> str:
    norm = ''.join(normalize_char(ch) for ch in key)
    if not norm or not norm.isalpha():
        raise ValueError('A chave deve conter somente letras e não pode ser vazia.')
    return norm


def caesar_encrypt(text: str, shift: int) -> str:
    shift %= 26
    out = []
    for ch in normalize_keep_nonletters(text):
        if ch in ALPHABET:
            out.append(ALPHABET[(ALPHABET.index(ch) + shift) % 26])
        else:
            out.append(ch)
    return ''.join(out)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


def validate_mono_key(key: str) -> str:
    key = normalize_keep_nonletters(key)
    if len(key) != 26 or not key.isalpha():
        raise ValueError('A chave monoalfabética deve ter exatamente 26 letras.')
    if len(set(key)) != 26:
        raise ValueError('A chave monoalfabética não pode conter letras repetidas.')
    return key


def mono_encrypt(text: str, key: str) -> str:
    key = validate_mono_key(key)
    table = str.maketrans(ALPHABET, key)
    return normalize_keep_nonletters(text).translate(table)


def mono_decrypt(text: str, key: str) -> str:
    key = validate_mono_key(key)
    table = str.maketrans(key, ALPHABET)
    return normalize_keep_nonletters(text).translate(table)


def vigenere_encrypt(text: str, key: str) -> str:
    key = only_letters_key(key)
    out, pos = [], 0
    for ch in normalize_keep_nonletters(text):
        if ch in ALPHABET:
            shift = ALPHABET.index(key[pos % len(key)])
            out.append(ALPHABET[(ALPHABET.index(ch) + shift) % 26])
            pos += 1
        else:
            out.append(ch)
    return ''.join(out)


def vigenere_decrypt(text: str, key: str) -> str:
    key = only_letters_key(key)
    out, pos = [], 0
    for ch in normalize_keep_nonletters(text):
        if ch in ALPHABET:
            shift = ALPHABET.index(key[pos % len(key)])
            out.append(ALPHABET[(ALPHABET.index(ch) - shift + 26) % 26])
            pos += 1
        else:
            out.append(ch)
    return ''.join(out)


def playfair_square(key: str) -> list[list[str]]:
    key = only_letters_key(key).replace('J', 'I')
    chars = []
    for ch in key + ALPHABET.replace('J', ''):
        if ch not in chars:
            chars.append(ch)
    return [chars[i:i + 5] for i in range(0, 25, 5)]


def playfair_prepare(text: str) -> str:
    letters = ''.join(ch for ch in normalize_keep_nonletters(text).replace('J', 'I') if ch in ALPHABET)
    pairs, i = [], 0
    while i < len(letters):
        a = letters[i]
        b = letters[i + 1] if i + 1 < len(letters) else 'X'
        if a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return ''.join(pairs)


def _pos(square, ch):
    for r, row in enumerate(square):
        if ch in row:
            return r, row.index(ch)
    raise ValueError(ch)


def _playfair(text: str, key: str, decrypt: bool = False) -> str:
    square = playfair_square(key)
    prepared = ''.join(ch for ch in normalize_keep_nonletters(text).replace('J', 'I') if ch in ALPHABET) if decrypt else playfair_prepare(text)
    step = -1 if decrypt else 1
    out = []
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i + 1]
        ra, ca = _pos(square, a)
        rb, cb = _pos(square, b)
        if ra == rb:
            out += [square[ra][(ca + step) % 5], square[rb][(cb + step) % 5]]
        elif ca == cb:
            out += [square[(ra + step) % 5][ca], square[(rb + step) % 5][cb]]
        else:
            out += [square[ra][cb], square[rb][ca]]
    return ''.join(out)


def playfair_encrypt(text: str, key: str) -> str:
    return _playfair(text, key, False)


def playfair_decrypt(text: str, key: str) -> str:
    return _playfair(text, key, True)


def encrypt(mode: int, text: str, key: str = '') -> str:
    if mode == 1:
        return text
    if mode == 2:
        return caesar_encrypt(text, int(key))
    if mode == 3:
        return mono_encrypt(text, key)
    if mode == 4:
        return playfair_encrypt(text, key)
    if mode == 5:
        return vigenere_encrypt(text, key)
    raise ValueError('Modo inválido')


def decrypt(mode: int, text: str, key: str = '') -> str:
    if mode == 1:
        return text
    if mode == 2:
        return caesar_decrypt(text, int(key))
    if mode == 3:
        return mono_decrypt(text, key)
    if mode == 4:
        return playfair_decrypt(text, key)
    if mode == 5:
        return vigenere_decrypt(text, key)
    raise ValueError('Modo inválido')
