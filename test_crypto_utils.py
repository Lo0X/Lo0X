import unittest
from crypto_utils import (
    caesar_decrypt, caesar_encrypt, mono_decrypt, mono_encrypt,
    playfair_decrypt, playfair_encrypt, validate_mono_key,
    vigenere_decrypt, vigenere_encrypt,
)


class CryptoUtilsTest(unittest.TestCase):
    def test_caesar(self):
        self.assertEqual(caesar_encrypt('Olá, tudo bem?', 3), 'ROD, WXGR EHP?')
        self.assertEqual(caesar_decrypt('ROD, WXGR EHP?', 3), 'OLA, TUDO BEM?')

    def test_mono(self):
        key = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        cipher = mono_encrypt('ABC XYZ!', key)
        self.assertEqual(cipher, 'QWE BNM!')
        self.assertEqual(mono_decrypt(cipher, key), 'ABC XYZ!')

    def test_invalid_mono_key(self):
        with self.assertRaises(ValueError):
            validate_mono_key('ABC')
        with self.assertRaises(ValueError):
            validate_mono_key('ABCDEFGHIJKLMNOPQRSTUVWXYA')

    def test_vigenere(self):
        cipher = vigenere_encrypt('ATAQUE AO AMANHECER!', 'SEGREDO')
        self.assertEqual(vigenere_decrypt(cipher, 'SEGREDO'), 'ATAQUE AO AMANHECER!')

    def test_playfair(self):
        cipher = playfair_encrypt('BALAO', 'SEGURANCA')
        self.assertEqual(len(cipher) % 2, 0)
        self.assertEqual(playfair_decrypt(cipher, 'SEGURANCA'), 'BALAOX')


if __name__ == '__main__':
    unittest.main()
