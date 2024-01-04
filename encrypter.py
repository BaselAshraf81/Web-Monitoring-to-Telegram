import sys
def encrypt(input_string):
    encrypted_string = ""
    for char in input_string:
        encrypted_string += chr(ord(char) + 10)
    return encrypted_string