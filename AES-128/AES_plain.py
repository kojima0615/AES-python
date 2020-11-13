import copy
import numpy as np


class AES:
    s_box = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    )

    inv_s_box = (
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
    )

    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    mix_culumns_table = (
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2],
    )

    inv_mix_culumns_table = (
        [14, 11, 13, 9],
        [9, 14, 11, 13],
        [13, 9, 14, 11],
        [11, 13, 9, 14]
    )

    def __init__(self, text, key):
        self.round = 10
        self.key_matrices = self.expand_key(key)  # 鍵
        #CPAで推定するとき(最終ラウンドで使う鍵を指定)
        '''
        temp = self.bytes2matrix(key)
        for i in range(4):
            for j in range(4):
                self.key_matrices[i][self.round*4+j] = temp[i][j]
        '''
        self.text = self.bytes2matrix(text)  # テキスト

    #128bitから4*4行列
    def bytes2matrix(self, k):
        kk = k
        res = []
        for i in range(4):
            res.append([])
        for i in range(4):
            for j in range(4):
                temp = (kk >> 8*(15-4*i-j)) % 256
                res[j].append(temp)
        return np.array(res)

    #4*4行列から128bit
    def matrixbytes2(self, m):
        ml = m.tolist()
        res = 0
        for i in range(4):
            for j in range(4):
                res += (ml[i][j] << (15-j*4-i)*8)
        return res

    #鍵スケジュール
    def expand_key(self, key):
        temp = self.bytes2matrix(key)
        res = np.zeros((4, 4*(self.round+1)), dtype=int)
        for i in range(4):
            for j in range(4):
                res[i][j] = temp[i][j]
        for k in range(self.round):
            for i in range(4):
                for j in range(4):
                    if j == 0:
                        if i == 0:
                            res[i][j + (k+1)*4] = res[0][(k+1)*4 -
                                                         4] ^ self.s_box[res[1][(k+1)*4-1]] ^ self.r_con[k+1]
                        else:
                            res[i][j + (k+1)*4] = res[i][(k+1)*4 -
                                                         4] ^ self.s_box[res[(i+1) % 4][(k+1)*4-1]]
                    else:
                        res[i][j + (k+1)*4] = res[i][(k+1)*4 +
                                                     j-4] ^ res[i][(k+1)*4+j-1]
        return np.array(res)

    def sub_bytes(self):
        for i in range(4):
            for j in range(4):
                self.text[i][j] = self.s_box[self.text[i][j]]
                #s_boxで置換

    def inv_sub_bytes(self):
        for i in range(4):
            for j in range(4):
                self.text[i][j] = self.inv_s_box[self.text[i][j]]
                #inv_s_boxで置換


    #最初のマッピングで向きを間違えたので転置してあります
    def shift_rows(self):
        s = self.text.T
        #一段目は動かさない
        #左巡回シフト
        #1つずらす
        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
        #2つずらす
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        #3つずらす
        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
        self.text = s.T

    def inv_shift_rows(self):
        s = self.text.T
        #一段目は動かさない
        #右巡回シフト
        s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
        self.text = s.T

    #GF(2) 1=-1
    #原子多項式 x^8+x^4+x^3+x+1
    #x^8=x^4+x^3+x+1
    def gmult(self, a, b):
        res = 0
        for _ in range(8):
            if b & 1 == 1:
                res ^= a
            flag = a & 0x80
            a <<= 1
            a &= 0xFF
            if flag == 0x80:
                a ^= 0x1b  # x^8=x^4+x^3+x+1
            b >>= 1
        return res

    #(4*4)*(4*1)の行列計算(暗号化)
    def mix_columns(self):
        temp = copy.deepcopy(self.text)
        for i in range(4):
            for j in range(4):
                temp[i][j] = 0
                for k in range(4):
                    temp[i][j] ^= self.gmult(
                        self.mix_culumns_table[i][k], self.text[k][j])
        self.text = temp

     #(4*4)*(4*1)の行列計算(復号化)
    def inv_mix_columns(self):
        temp = copy.deepcopy(self.text)
        for i in range(4):
            for j in range(4):
                temp[i][j] = 0
                for k in range(4):
                    temp[i][j] ^= self.gmult(
                        self.inv_mix_culumns_table[i][k], self.text[k][j])
        self.text = temp

    #生成した鍵とXOR
    def add_round_key(self, k):
        for i in range(4):
            for j in range(4):
                self.text[i][j] ^= self.key_matrices[i][j+k*4]

    #暗号化
    def encryption(self):
        self.add_round_key(0)
        print(self.text)
        for i in range(self.round-1):
            self.sub_bytes()

            self.shift_rows()

            self.mix_columns()
            self.add_round_key(i+1)
            print(self.text)
        self.sub_bytes()
        self.shift_rows()
        self.add_round_key(self.round)
        print(self.text)
        return self.matrixbytes2(self.text)

    #復号化
    def decryption(self):
        self.add_round_key(self.round)
        self.inv_shift_rows()
        self.inv_sub_bytes()
        for i in range(self.round-1):
            self.add_round_key(self.round-i-1)
            self.inv_mix_columns()
            self.inv_shift_rows()
            self.inv_sub_bytes()
        self.add_round_key(0)
        return self.matrixbytes2(self.text)

    #10ラウンドだけ復号
    def decryption_oneround_a(self):
        print(self.matrixbytes2(self.text))
        self.add_round_key(self.round)
        print(self.matrixbytes2(self.text))
        self.inv_shift_rows()
        print(self.matrixbytes2(self.text))
        self.inv_sub_bytes()
        print(self.matrixbytes2(self.text))
        self.shift_rows()
        return self.matrixbytes2(self.text)


def main():
    a = 0x00112233445566778899aabbccddeeff
    b = 0x000102030405060708090a0b0c0d0e0f
    aes = AES(a, b)
    c = aes.encryption()
    print(hex(c))

    aes1 = AES(c, b)
    d = aes1.decryption()
    print(hex(d))


if __name__ == "__main__":
    main()