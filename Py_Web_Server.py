import socket
import string
import os


def create_socket():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    sock.bind((ip_address, 80))
    sock.listen()

    return sock


def http_handler(connection, request):
    
    method = request.partition(' ') # basic parsing of HTTP request header
    request_uri = method[2].partition(' ')

    if method[0] == 'GET': # only accepts GET requests at the moment
        result = enumerate_files(request_uri[0])
        if result[0] == True:
            if result[1] == 'html': # only supporting html and css resources at the moment
                connection[0].send((text_html + result[2]).encode())
                connection[0].close()
            elif result[1] == 'css':
                connection[0].send((text_css + result[2]).encode())
                connection[0].close()
        else:
            result = open_file('404.html')
            connection[0].send((http_404 + result[1]).encode())
            connection[0].close()
    else:
        result = open_file('405.html')
        connection[0].send((http_405 + result[1]).encode()) # 405 Method Not Allowed if requested method other than GET
        connection[0].close()


def enumerate_files(request_uri):

    file_exists = False
    file_type = None
    file_data = None

    if request_uri == '/':
        file_exists = True
        file_type, file_data = open_file('index.html') # treating index.html as default page
    else:
        request_uri = request_uri.strip('/')
        for directory, subdirectory, files in os.walk("C:/"): # change directory to your web server directory
            os.chdir(directory)
            if request_uri in files:
                file_exists = True
                file_type, file_data = open_file(request_uri)
                break

    return file_exists, file_type, file_data


def open_file(file_name):

    file = open(file_name, 'r')
    file_data = file.read()
    file.close()

    file_type = file_name.split('.')[1]

    return file_type, file_data


if __name__ == "__main__":

    text_html = 'HTTP/1.1 200 OK\n' + 'Content-Type: text/html\n' + 'Connection: close\n' + '\n' # a more robust system for generating the HTTP headers on the fly is needed
    text_css = 'HTTP/1.1 200 OK\n' + 'Content-Type: text/css\n' + 'Connection: close\n' + '\n'

    http_404 = 'HTTP/1.1 404 File Not Found\n' + 'Content-Type: text/html\n' + 'Connection: close\n' + '\n'
    http_405 = 'HTTP/1.1 405 Method Not Allowed\n' + 'Content-Type: text/html\n' + 'Connection: close\n' + '\n'

    sock = create_socket()

    while 1:
        connection = sock.accept()
        request = connection[0].recv(1024).decode()
        print(request)
        http_handler(connection, request)