# secure-telnet-dfhm
This is the code for a custom encrypted TCP communication channel, that uses Diffie Hellman Merkle from scratch.

# Run the encrypted server
Usage: python telnet_secure_server.py {HOST IP} {PORT}

# Connect as a client
Usage: python telnet_secure.py {HOST IP} {PORT}

This supports multiple client connection threads, with unique session key generation using DFHM algorithm, then encrypts/decrypts the two way communication once it sends to/arrives on the server machine, and each client machine.
