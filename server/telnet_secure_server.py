import socket
import select
import _thread
import telnetlib
import blowfish
import argparse
import time
import os
import sys
sys.path.append('../')
from binding import prime
divider = "=" * 100
margin = " " * 5

# TODO: format this into a package that can be used as a command line tool
# https://trstringer.com/easy-and-nice-python-cli/

class Telnet_s_server:
  def __init__(self, host, port, private_key):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s_host = host
    self.s_port = port
    self.private_key = private_key
    self.public_key = 0
    self.cipher = 0
    self.shared_base = 0
    self.shared_modulus = 0
    self.client_connections = []
    self.client_threads = []

  def run(self):
    while True:

      # We have a visitor
      client, client_ip = self.sock.accept()

      # Log into the global thread tracker
      # Passing in sock info from this connection
      self.announce(client_ip)
      self.client_handler(client, client_ip)

  def client_handler(self, client, client_ip):
    _thread.start_new_thread(secure_server.client_thread,(client,client_ip))


  def announce(self, client_id):
    print(f"{divider}\n{client_id[0]}:{client_id[1]} has connected.\n{divider}\n")

  def cipher_setup(self, session_key):
    # The key passed in needs to be between 4 and 56 bytes
    session_key=str(session_key)
    if (len(session_key)<4):
      for x in range(4-len(session_key)):
        session_key+=" "
    elif (len(session_key)>56):
      session_key[:56]

    cipher_little = blowfish.Cipher(session_key.encode(), byte_order = "little")
    # This can't be global, otherwise session key will be shared with other threads
    # TODO: fix it!!
    self.cipher = cipher_little

  def generate_session_key(self, client_public_key, shared_modulus):
    return (client_public_key**self.private_key)%shared_modulus

  def decrypt(self, msg):
    msg=msg.decode()
    msg=eval(r'{}'.format(msg))
    msg=self.cipher.decrypt_ecb(msg)
    msg=b"".join(msg)
    msg=msg.decode()

    return msg

  def encrypt(self, msg):

    # In order to use blowfish encryption, the message needs to be in a multiple of     8
    if len(msg)<8:
      for x in range(8-len(msg)):
        msg+=" "
    else:
      for x in range(8-(len(msg)%8)):
        msg+=" "

    msg=msg.encode()
    #print("msg.encode()", msg, type(msg))
    block=bytearray(msg)
    #print("byte(array)", block, type(block))
    #cipher_little = blowfish.Cipher(b"my key", byte_order = "little")
    #print("encrypt_ecb()", self.cipher.encrypt_ecb(block), type(self.cipher.encrypt    _ecb(block)))
    data_encrypted = b"".join(self.cipher.encrypt_ecb(block))
    #print("data_encrypted", data_encrypted, type(data_encrypted))

    #data_decrypted = b"".join(self
    #.cipher.decrypt_ecb(b"".join(self.cipher.encrypt_ecb(block))))
    #data_decrypted = b"".join(self.cipher.decrypt_ecb(data_encrypted))
    #print("data_decrypted", data_decrypted, type(data_decrypted))

    return data_encrypted

  def setup(self):
    try:
      # this is a socket object, AF_INET is address family for IPv4, SOCK_STREAM is mechanism for 2 way, ordered, unduplicated byte stream
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((self.s_host, int(self.s_port)))
      # bind the socket object to a host & port
      self.sock.listen(3)

    except:
      print(f"ERROR: socket setup failure. Exiting now.\n")
      exit()

  def generate_prime(self):
    # TODO: get these values below from a server config file
    max_int = 3000
    min_sig_fig = 3
    return prime.generate_sieve_prime(max_int,min_sig_fig)

  def session_shared_primes(self):
    self.shared_base = self.generate_prime()
    time.sleep(1)
    self.shared_modulus = self.generate_prime()

    # This formatted string will be shared with the client
    return f"shared_base:{self.shared_base},shared_modulus:{self.shared_modulus}\n"

  def client_thread(self,client,client_ip):
    # The Diffie-Hellman-Merkel algorithm starts here
    self.client_threads.append(client)

    # Generate fresh public prime numbers to share with this client
    session_values=self.session_shared_primes()
    print(f"We picked {session_values} for {client_ip}")
    """client.send(session_values.encode())

    # Generate public key using shared value, share with clients
    self.public_key = (self.shared_base**self.private_key)%self.shared_modulus
    # TODO: Write explanation for the new line
    print("Sending to client our public key: ", self.public_key)
    formatted_public_key = str(self.public_key)+"\n"
    client.send(formatted_public_key.encode())

    # Receive client's public key
    client_public_key=int(client.recv(2048).decode())
    print("Client's public key is:", client_public_key)

    # This is destroyed upon terminating the client thread
    session_key=self.generate_session_key(client_public_key, self.shared_modulus)
    print("Ephemeral Session Key has been generated:", session_key)
    self.cipher_setup(session_key)

    # Two-way channel is now encrypted with our session key generated by the DFHM algorithm
    alive=True
    while alive:
      # <bytes>
      message=client.recv(2048)
      if message:
        print("\n[" + client_ip[0] + "]: " + message.decode()[2:-1])
        data_decrypted = self.decrypt(message)
        print("[" + client_ip[0] + "]: " + data_decrypted)

      else:
        self.remove_thread(client, client_ip[0])
        alive=False
      send_to_client = input('telnet secure> ')
      send_to_client = str(self.encrypt(send_to_client)) + "\n"
      #client.send(str(send_to_client).encode())
      client.send(send_to_client.encode())
    exit()"""

  def remove_thread(self, client, client_ip):

    if client in self.client_threads:
      self.client_threads.remove(client)
    divider(80)
    print (client_ip + " has exited")
    divider(80)
    exit()

# ============================================================
# SERVER SET UP FUNCTIONS
# ============================================================

def welcome_banner():
    print(f"{divider}\n\n{margin}Booting Up Secure Telnet Server v1.0.0")
    print(f"{margin}Author: Claire Y. Li\n")
    print(f"{divider}")

def get_server_default_gateway():
    import netifaces
    # 2 is AF_INET (normal Internet addresses)
    gws = netifaces.gateways()
    try:
        default_gate = gws['default'][netifaces.AF_INET][0]
        if default_gate:
            print(default_gate)
            return default_gate
    except:
        print("ERROR")

    #return gws['default'][netifaces.AF_INET][0]

def get_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bridge to the internet
    default_gateway = get_server_default_gateway()
    s.connect((default_gateway, 80))

    host = s.getsockname()[0]
    s.close()

    return host

# ============================================================
# Wait for client(s) to connect
# ============================================================
if __name__ == '__main__':
    # TODO: add logging...
    welcome_banner()

    # valid: python3 telnet_secure_server.py 9090
    parser = argparse.ArgumentParser(description='Set up the secure telnet server')
    parser.add_argument("port", type=int, help="port")
    args = parser.parse_args()

    server_info = {}

    # TODO: combine try excepts, but see what industry standard is, should i be mashing a bunch of different exxceptions into the same block?
    try:
        host = get_host()
        assert type(host) == str
        server_info = {'host': host, 'port': args.port}
    except AssertionError:
        print(f"\nERROR: Setup procedure failed. Exiting.\n")
        exit()

    try:
        print(f"\nLoading server private key.")
        with open('server.private.key','r') as k:
            private_key=k.read()
    except FileNotFoundError:
        print(f"ERROR: Server is missing a private key. \nPlease create a file at: {os.getcwd()}/server.private.key\nIt must contain an integer, no spaces, no decimals or special characters.\n")
        sys.exit(1)

    # invalid private key value, needs to be an integer
    try:
        private_key = int(private_key)
        # TODO: add another check to make sure its a prime number
    except ValueError:
        print(f"ERROR: Server private key file has an invalid value: {private_key}")
        print(f"You need to delete that value.\nReplace it with a prime integer of your choice.\n")
        sys.exit(1)

    secure_server = Telnet_s_server(server_info['host'], server_info['port'], private_key)
    secure_server.setup()
    secure_server.run()

    """while True:




      # Set up two-way encrypted TCP tunnel
      _thread.start_new_thread(secure_server.client_thread,(client,client_ip))

      # TODO: if user inputs shutdown, close server, log off

    client.close()
    server.close()"""
