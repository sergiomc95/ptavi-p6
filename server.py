#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import sys
import socketserver
import os

try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    AUDIO = sys.argv[3]

except UsageError:
    print("Usage: python server.py IP port audio_file")


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        """handle."""
        while 1:
            METODOS = ['INVITE', 'ACK', 'BYE']
            line = self.rfile.read()
            linea = line.decode('utf-8')
            METODO = linea.split(' ')[0]
            print("El cliente nos manda " + linea)

            if not line:
                break
            if METODO == 'INVITE':
                print("El cliente nos manda" + line.decode('utf-8'))
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n" +
                                 b"SIP/2.0 180 Ring\r\n\r\n" +
                                 b"SIP/2.0 200 OK\r\n\r\n")

            elif METODO == 'ACK':
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)

            elif METODO == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif METODO not in METODOS:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request")


if __name__ == "__main__":
    if not os.path.exists(AUDIO):
        raise OSError
    if len(sys.argv) != 4:
        raise IndexError
    serv = socketserver.UDPServer((IP, int(PORT)), EchoHandler)
    print("Listening....")
    serv.serve_forever()
