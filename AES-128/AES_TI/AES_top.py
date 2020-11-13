import encryption


def main():
    #plain = 0x10123456789abcde10123456789abcde
    plain = 0x00112233445566778899aabbccddeeff
    key = 0x000102030405060708090a0b0c0d0e0f
    temp = encryption.enc(plain,key)
    print(hex(temp))



if __name__ == "__main__":
    main()
