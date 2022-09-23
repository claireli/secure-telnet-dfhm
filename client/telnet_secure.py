import telnetlib
import subprocess
import blowfish
import argparse
import socket
import sys
sys.path.append('../')
import os

divider = "=" * 100
margin = ' ' * 5

class Telnet_s:
  def __init__(self, destination_host, destination_port, timeout, private_key):
    self.d_host = destination_host
    self.d_port = destination_port
    self.timeout = timeout
    self.s_host = "127.0.0.1"
    self.private_key = private_key
    self.public_key = None
    self.cipher = None
    self.session = None

  def cipher_setup(self, session_key):
    # The key passed in needs to be between 4 and 56 bytes
    if (len(session_key)<4):
      for x in range(4-len(session_key)):
        session_key+=" "
    elif (len(session_key)>56):
      session_key=session_key[:56]

    cipher_little = blowfish.Cipher(session_key.encode(), byte_order = "little")
    self.cipher = cipher_little

  def decrypt(self, msg):
    msg=msg.decode()
    msg=eval(r'{}'.format(msg))
    msg=self.cipher.decrypt_ecb(msg)
    msg=b"".join(msg)
    msg=msg.decode()

    return msg

  def encrypt(self, msg):
    # In order to use blowfish encryption, the message needs to be in a multiple of 8
    if len(msg)<8:
      for x in range(8-len(msg)):
        msg+=" "
    else:
      for x in range(8-(len(msg)%8)):
        msg+=" "

    print(msg, type(msg))
    msg=msg.encode()
    print(msg, type(msg))
    block=bytearray(msg)
    print(block, type(block))
    data_encrypted = b"".join(self.cipher.encrypt_ecb(block))
    print(data_encrypted)
    return data_encrypted

  def generate_session_key(self, server_public_key, shared_modulus):
    return (server_public_key**self.private_key)%shared_modulus

  def public_key_handler(self):
      message = self.session.read_until(b'\n')
      print(message)

  def connect_to_remote(self):
    try:
      self.session = telnetlib.Telnet(self.d_host, self.d_port, self.timeout)
    except ConnectionRefusedError:
      print(f"ERROR: Target server is not online, {self.d_host}:{self.d_port}\n")
      # TODO: write method for standard exit steps
      exit()

    self.public_key_handler()

    """try:
        with telnetlib.Telnet(self.d_host, self.d_port, self.timeout) as session:
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

            # Two-way channel is now encrypted with our session key generated by the DFHM algorithm
            alive=True
            while alive:
              send_to_remote = input('telnet secure> ')
              if send_to_remote == "quit" or send_to_remote == "^]":
                exit()
              else:
                send_to_remote = self.encrypt(send_to_remote)

              session.write(str(send_to_remote).encode())
              # <bytes>
              message = session.read_until(b'\n')
              if message:
                print("\n[" + self.d_host + "]: " + message.decode()[2:-1])
                data_decrypted = self.decrypt(message)
                print("[" + self.d_host + "]: " + data_decrypted)
                #print("\n[192.168.1.126]: " + message.decode()[2:-1])
                #data_decrypted = self.decrypt(message)
                #print("[192.168.1.126]: " + data_decrypted)

              else:
                self.remove_thread(client, client_ip[0])
                alive=False
    except socket.error:
        print(f"Provided host and port of {self.d_host}, {self.d_port} is not online")
        sys.exit(1)"""

# ============================================================
# CLIENT SET UP FUNCTIONS
# ============================================================

def welcome_banner():
    print(f"""{divider}\n\n{margin}Launching Secure Telnet Server Client v1.0.0\n{margin}Author: Claire Y. Li\n\n{margin}To see the writeup on this project, go to eclairbytes.com\n\n{divider}\n""")

def setup_target(ip, port):
    if not ip:
        print(f"\nMissing: You will need to specify the host of the telnet server.")
        ip = str(input(f"Target Host: "))

    if not port:
        print(f"\nMissing: You will need to specify the port of the telnet server.")
        port = str(input(f"Target Port: "))
    return {'host':ip,'port':port}


if __name__ == '__main__':
    # TODO: add logging...
    welcome_banner()

    parser = argparse.ArgumentParser(description='Launch the client for the secure telnet server')
    parser.add_argument('--ip')
    parser.add_argument('--port')

    destination_info = {}

    try:
        # None and None = no ip and no port passed in, None and None == None
        # None and str = no ip and a port passed in, None and "hi" == None
        # str and None = ip and no port passed in, "hi" and None == None
        # str and str = ip and port passed in, "hi" and "hello" ==
        # When I do an AND op on two differing data types together, the truth table will look like this:
        # "hi" AND "hello" == "hello"
        # "hello" AND "hi" == "hi"
        # "hi" and None == None

        # The possible combos from type(a and b) are the set {str, None}
        # There are 3 cases where it is None.
        # assert None != None results in
        # not None is True
        # not Str is False
        assert type(parser.parse_args().ip and parser.parse_args().port) == str
        destination_info = {'host': parser.parse_args().ip, 'port': parser.parse_args().port}

    except AssertionError:
        print("ASS ERROR")
        destination_info = setup_target(parser.parse_args().ip, parser.parse_args().port)
#    finally:
#        print(f"Initiating connection to {destination_info['host']}:{destination_info['port']}")
    # Set up for host, port, timeout, load private key, valid private key
    # user shouldn't decide this, move this to a config file
    timeout = 100

    # try catch exception for missing private key
    # stdout, put new line at the front for info
    # but put new line at the end if its an error message and exit
    try:
        print(f"\nLoading your private key.")
        with open('client.private.key','r') as k:
            private_key=k.read()
    except FileNotFoundError:
        print(f"ERROR: You are missing your private key. \nPlease create a file at: {os.getcwd()}/client.private.key\nIt must contain an integer, no spaces, no decimals or special characters.\n")
        sys.exit(1)

    # invalid private key value, needs to be an integer
    try:
        private_key = int(private_key)

        # TODO: add another check to make sure its a prime number
    except ValueError:
        print(f"ERROR: Your private key file has an invalid value: {private_key}")
        print(f"You need to delete that value.\nReplace it with a prime integer of your choice.\n")
        sys.exit(1)

    connection = Telnet_s(destination_info['host'], destination_info['port'], timeout, private_key)
    connection.connect_to_remote()