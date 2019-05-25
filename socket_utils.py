#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/struct.html
import socket
import json
import struct


class SocketUtils:
    """
    Utility class for sending data via sockets

    """
    @staticmethod
    def sendJson(socket, object):
        """
        Sends a dictionary in JSON format through a given socket

        Args:
            socket (socket): The socket to send data through
            object (dict): Dictionary object to JSONify and send

        """
        jsonString = json.dumps(object)
        data = jsonString.encode("utf-8")
        jsonLength = struct.pack("!i", len(data))
        socket.sendall(jsonLength)
        socket.sendall(data)

    @staticmethod
    def recvJson(socket):
        """
        Receives a JSON object via socket and returns it as a dictionary

        Args:
            socket (socket): The socket to send data through

        Returns:
            Dictionary object generated from received JSON data

        """
        buffer = socket.recv(4)
        jsonLength = struct.unpack("!i", buffer)[0]

        # Reference: https://stackoverflow.com/a/15964489/9798310
        buffer = bytearray(jsonLength)
        view = memoryview(buffer)
        while jsonLength:
            nbytes = socket.recv_into(view, jsonLength)
            view = view[nbytes:]
            jsonLength -= nbytes

        jsonString = buffer.decode("utf-8")
        return json.loads(jsonString)

# IMPORTANT NOTE: THIS FILE IS USED TO TEST FUNCTIONALITY AND WAS PROVIDED
# BY MATHEW BOLGER 'TUTE 8'
