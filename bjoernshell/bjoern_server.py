import socket


class BjoernConnection(object):
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = host
        self._port = port

    def connect(self):
        self.socket.connect((self.host, self.port))

    def request(self, request):
        request = "{}\0".format(request.strip())
        request = request.encode()
        self.socket.sendall(request)

    def response(self):
        response = b""
        while True:
            chunk = self.socket.recv(2048)
            response += chunk
            try:
                if response[-1] == 0x00:
                    break
            except:
                pass

        response = response[:-1].decode().strip()
        return response


    def close(self):
        self._socket.close()

    @property
    def socket(self):
        return self._socket

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port


class BjoernInterface(object):
    def __init__(self, connection):
        self._connection = connection

    def run(self, command):
        self.connection.request(command)
        return self.connection.response()

    def get_stepnames(self):
        response = self.run("Gremlin.getStepNames()")
        steps = response.split('\n')
        return steps

    def get_variables(self):
        response = self.run("getBinding().getVariables().keySet()")
        variables = response.split('\n')
        return variables

    @property
    def connection(self):
        return self._connection
