import sys
import os
import telnetlib
import subprocess
import blowfish

class Telnet_s:
  def __init__(self, destination_host, destination_port, timeout, private_key):
    self.dhost = destination_host
    self.dport = destination_port
    self.timeout = timeout
    self.shost = "127.0.0.1"
    self.private_key = private_key
    self.public_key = 0
    self.cipher = 0

  def cipher_setup(self, session_key):
    # The key passed in needs to be between 4 and 56 bytes
    if (len(session_key)<4):
      for x in range(4-len(session_key)):
        session_key+=" "
    elif (len(session_key)>56):
      session_key=session_key[:56]

    cipher_little = blowfish.Cipher(session_key.encode(), byte_order = "little")
    self.cipher = cipher_little

  def encrypt(self, msg):
    
    # In order to use blowfish encryption, the message needs to be in a multiple of 8
    if len(msg)<8:
      for x in range(8-len(msg)):
        msg+=" "
    else:
      for x in range(8-(len(msg)%8)):
        msg+=" "
    
    msg=msg.encode()
    print("msg.encode()", msg, type(msg))
    block=bytearray(msg)
    print("byte(array)", block, type(block))
    #cipher_little = blowfish.Cipher(b"my key", byte_order = "little")
    print("encrypt_ecb()", self.cipher.encrypt_ecb(block), type(self.cipher.encrypt_ecb(block)))
    data_encrypted = b"".join(self.cipher.encrypt_ecb(block))
    print("data_encrypted", data_encrypted, type(data_encrypted))

    data_decrypted = b"".join(self
.cipher.decrypt_ecb(b"".join(self.cipher.encrypt_ecb(block))))
    #data_decrypted = b"".join(self.cipher.decrypt_ecb(data_encrypted))    
    print("data_decrypted", data_decrypted, type(data_decrypted))
 
    return data_encrypted

  def generate_session_key(self, server_public_key, shared_modulus):
    return (server_public_key**self.private_key)%shared_modulus

  def connect_to_remote(self):
    with telnetlib.Telnet(self.dhost, self.dport, self.timeout) as session:
        # Receive the shared public values from server
        message = session.read_until(b'\n') 
        shared_base=int(message.decode().split(",")[0].split(":")[1])
        shared_modulus=int(message.decode().split(",")[1].split(":")[1])

        # Your public key
        self.public_key = (shared_base**self.private_key)%shared_modulus
        session.write(str(self.public_key).encode())
        
        # Recieve public key from server
        # This is destroyed upon disconnecting the thread
        message = session.read_until(b'\n')
        server_public_key = int(message.decode())

        print("Server's public key is", server_public_key)

        # This is destroyed upon disconnecting the thread
        session_key=self.generate_session_key(server_public_key, shared_modulus)
        
        print("Ephemeral Session Key has been generated.", session_key)
        self.cipher_setup(str(session_key))

        while True:

          send_to_remote = input('telnet secure> ')

          if send_to_remote == "quit" or send_to_remote == "^]":
            exit()
          else:
            send_to_remote = self.encrypt(send_to_remote)

          print("send_to_remote", send_to_remote, type(send_to_remote))
          print("str(send_to_remote).encode()", str(send_to_remote).encode(), type(str(send_to_remote).encode()))
          #print("send_to_remote.encode()", send_to_remote.encode(), type(send_to_remote).encode())
          #print("session.write()", str(send_to_remote.encode()), type(str(send_to_remote).encode()))

          session.write(str(send_to_remote).encode())
# ============================================================
ip = str(sys.argv[1])
port = int(sys.argv[2])
timeout = 100

with open("client.private.key","r") as k:
  private_key=int(k.read())

connection = Telnet_s(ip, port, timeout, private_key)
connection.connect_to_remote()
