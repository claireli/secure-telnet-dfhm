import blowfish
import os

class DFHM:
  def __init__(self, key):
    self.client_key = key
    self.session_key = self.request_session_key()
    # The key passed in needs to be between 4 and 56 bytes
    self.cipher = self.cipher_setup()
    self.byte = ' '

  def request_session_key(self):
      return '7231key'

  def cipher_setup(self):
    # The session key provided to blowfish encryption needs to be a multiple of four
    if (len(self.session_key)<4):
      for x in range(4-len(self.session_key)):
        self.session_key = f'{self.session_key}{self.byte}'
    elif (len(self.session_key)>56):
      self.session_key[:56]

    cipher_little = blowfish.Cipher(self.session_key.encode('utf-8'), byte_order = 'little')
    return cipher_little

  def encrypt(self, block):
    print('1. BLOCK', block, type(block), len(block))

    message=block.encode()
    print('2. ENCODED BLOCK', message, type(message), len(message))

    data_encrypted = b''.join(self.cipher.encrypt_ecb(message))
    #print(message, type(message))
    print('3. ENCRYPTED', data_encrypted, type(data_encrypted), len(data_encrypted))
    return data_encrypted


    #print(data_encrypted)

# methods
# determine shared prime
# determine shared modulus
# encrypt with session key
# decrypt with session key
