from ..proto.block_cipher import BlockCipher


class DESCipher(BlockCipher):
    IP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    # Final Permutation Table
    # NOTE: This is the inverse of IP table, and it's pretty regular :)
    FP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]

    # Expansion Table
    E = [
        32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11,
        12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29,
        30, 31, 32, 1
    ]

    # S-boxes
    S_BOXES = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        # S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],
        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],
        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],
        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

    # Permutation Table
    P = [
        16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25
    ]

    # PC-1 Table
    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]

    # PC-2 Table
    PC2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    # Left Rotations Table
    LEFT_ROTATIONS = [
        1, 1, 2, 2, 2, 2, 2, 2,
        1, 2, 2, 2, 2, 2, 2, 1
    ]

    def __init__(self, key: str) -> None:
        super().__init__(key)
        # Initial Permutation Table
        self.round_keys = self.generate_round_keys(key)

    def generate_round_keys(self, key: str) -> list[str]:
        key = self.permute(self.PC1, self._str_to_bin(key)[:64])
        left, right = key[:28], key[28:]
        round_keys = []

        for rotation in self.LEFT_ROTATIONS:
            left = left[rotation:] + left[:rotation]
            right = right[rotation:] + right[:rotation]
            round_keys.append(self.permute(self.PC2, left + right))

        return round_keys

    def permute(self, table: list[int], block: str) -> str:
        return ''.join(block[i - 1] for i in table)

    def initial_permutation(self, text: str) -> str:
        return self.permute(self.IP, text)

    def final_permutation(self, text: str) -> str:
        return self.permute(self.FP, text)

    def process(self, text: str, round_keys: list[str]) -> str:
        left, right = text[:32], text[32:]
        for round_key in round_keys:
            expanded_right = self.permute(self.E, right)
            xored = self._xor(expanded_right, round_key)
            substituted = self._substitute(xored)
            permuted = self.permute(self.P, substituted)
            left, right = right, self._xor(left, permuted)
        return right + left

    def bin_to_bin_encrypt(self, bin_plaintext: str) -> str:
        # Initial Permutation
        permuted_text = self.initial_permutation(bin_plaintext)
        # 16 rounds of processing
        processed_text = self.process(permuted_text, self.round_keys)
        # Final Permutation
        bin_ciphertext = self.final_permutation(processed_text)
        return bin_ciphertext

    def encrypt(self, plaintext: str) -> str:
        '''
        Encryption Process
        Input: readable plaintext
        Output: hexadecimal ciphertext
        '''
        bin_plaintext = self._str_to_bin(plaintext)
        bin_ciphertext = self.bin_to_bin_encrypt(bin_plaintext)
        hex_ciphertext = self._bin_to_hex(bin_ciphertext)
        return hex_ciphertext

    def bin_to_bin_decrypt(self, bin_ciphertext: str) -> str:
        # Initial Permutation
        permuted_text = self.initial_permutation(bin_ciphertext)
        # 16 rounds of processing
        processed_text = self.process(permuted_text, self.round_keys[::-1])
        # Final Permutation
        bin_plaintext = self.final_permutation(processed_text)
        return bin_plaintext

    def decrypt(self, ciphertext: str) -> str:
        '''
        Decryption Process
        Input: hexadecimal ciphertext
        Output: readable plaintext
        '''
        bin_ciphertext = self._hex_to_bin(ciphertext)
        bin_plaintext = self.bin_to_bin_decrypt(bin_ciphertext)
        plaintext = self._bin_to_str(bin_plaintext)
        return plaintext

    def _substitute(self, text: str) -> str:
        result = []
        for i in range(8):
            block = text[i*6:(i+1)*6]
            row = int(block[0] + block[-1], 2)
            col = int(block[1:5], 2)
            result.append(format(self.S_BOXES[i][row][col], '04b'))
        return ''.join(result)

    def _xor(self, a: str, b: str) -> str:
        return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

    def _str_to_bin(self, text: str) -> str:
        return ''.join(format(ord(char), '08b') for char in text)

    def _bin_to_hex(self, binary: str) -> str:
        hex_string = hex(int(binary, 2))[2:]
        return hex_string.upper()

    def _hex_to_bin(self, hex_string: str) -> str:
        return bin(int(hex_string, 16))[2:].zfill(64)

    def _bin_to_str(self, binary: str) -> str:
        chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
        return ''.join(chars)

if __name__ == "__main__":
    key = "yjsnpy64"
    des = DESCipher(key)
    plaintext = "64bblock"
    encrypted = des.encrypt(plaintext)
    print(f"Encrypted: {encrypted}")
    decrypted = des.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
