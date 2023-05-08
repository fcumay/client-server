import socket
import os
from loguru import logger

logger.add("debugserver.log", format="{time} {level} {message}", level="DEBUG")

# HOST = '127.0.0.1'  # ip адрес сервера
# PORT = 7000  # порт сервера
HOST = '192.168.100.77'
PORT = 7000
DIRECTORY_NAME = "D:\\distribute"  # путь к папке с файла ми


def serve_file(filename: str) -> bin:
    '''Возвращает содержание файла в бинарном формате для всех файлов, кроме .txt'''
    try:
        with open(f"{DIRECTORY_NAME}\\{filename}", 'rb') as f:
            file_content = f.read()
            _, file_extension = os.path.splitext(filename)
            if file_extension == '.txt':
                file_content = file_content.decode('utf-8')
                file_content = file_content.encode('cp1251')
            logger.info(f'Read {file_extension} file')
            return file_content
    except IOError:
        logger.warning(f'{filename} not found in {DIRECTORY_NAME}')
        return logger.warning(f'{filename} not found in {DIRECTORY_NAME}')


# def handle_request(request):
#     '''Обрабатывает запрос к серверу'''
#     if b'\r\n\r\n' in request:
#         headers, body = request.split(b'\r\n\r\n', 1)  # \r\n\r\n - разделяет заголовок с телом запроса
#         method, path, protocol = headers.split(b'\r\n')[
#             0].split()  # разбиваем первую строку заголовка на соответствующие параметры
#         filename = path.decode('utf-8')[1:]
#         logger.info(f'{method},{path},{protocol}')
#         if method == b'GET':
#             _, file_extension = os.path.splitext(filename)
#             if file_extension == '.html':
#                 with open(os.path.join(DIRECTORY_NAME, filename), 'r', encoding='utf-8') as f:
#                     html_content = f.read()
#                 response_body = html_content.encode('utf-8')
#                 response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.format(
#                     len(response_body)).encode('utf-8')
#                 logger.info(f'GET .html : {response_headers}')
#             elif file_extension in ('.png', '.jpg', '.jpeg'):
#                 response_body = serve_file(filename)
#                 response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: image/png; charset=utf-8\r\n\r\n'.format(
#                     len(response_body)).encode('utf-8')
#                 logger.info(f'GET .png||.jpg||.jpeg : {response_headers}')
#             else:
#                 response_body = serve_file(filename)
#                 response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n'.format(len(response_body)).encode(
#                     'utf-8')
#                 logger.info(f'GET  {response_headers}')
#             if response_body:
#                 response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n'.format(
#                     len(response_body)).encode(
#                     'utf-8')
#                 response = response_headers + response_body
#             else:
#                 response_headers = 'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n'.encode('utf-8')
#                 response = response_headers
#             return response
#
#         elif method == b'POST':
#             with open(os.path.join(DIRECTORY_NAME, filename), 'wb') as f:
#                 f.write(body)
#             logger.info(f'POST in {filename} successfully')
#             return b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n'
#         elif method == b'OPTIONS':
#             response_headers = 'HTTP/1.1 200 OK\r\nAllow: GET, POST, OPTIONS\r\nContent-Length: 0\r\n\r\n'.encode(
#                 'utf-8')
#             return response_headers
#     else:
#         logger.warning(f'Bad requests structure')
#         return b'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n'
def handle_request(request):
    '''Обрабатывает запрос к серверу'''
    if b'\r\n\r\n' in request:
        headers, body = request.split(b'\r\n\r\n', 1)  # \r\n\r\n - разделяет заголовок с телом запроса
        method, path, protocol = headers.split(b'\r\n')[
            0].split()  # разбиваем первую строку заголовка на соответствующие параметры
        filename = path.decode('utf-8')[1:]
        logger.info(f'{method},{path},{protocol}')
        if method == b'GET':
            _, file_extension = os.path.splitext(filename)
            if file_extension == '.html':
                with open(os.path.join(DIRECTORY_NAME, filename), 'r', encoding='utf-8') as f:
                    html_content = f.read()
                response_body = html_content.encode('utf-8')
                response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.format(
                    len(response_body)).encode('utf-8')
                logger.info(f'GET .html : {response_headers}')
            elif file_extension in ('.png', '.jpg', '.jpeg'):
                response_body = serve_file(filename)
                if response_body is not None:
                    response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: image/png; charset=utf-8\r\n\r\n'.format(
                        len(response_body)).encode('utf-8')
                    logger.info(f'GET .png||.jpg||.jpeg : {response_headers}')
                else:
                    response_headers = 'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n'.encode('utf-8')
                    logger.warning(f'{filename} not found in {DIRECTORY_NAME}')
                    return response_headers
            else:
                response_body = serve_file(filename)
                if response_body is not None:
                    response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n'.format(len(response_body)).encode(
                        'utf-8')
                    logger.info(f'GET  {response_headers}')
                else:
                    response_headers = 'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n'.encode('utf-8')
                    logger.warning(f'{filename} not found in {DIRECTORY_NAME}')
                    return response_headers

            response = response_headers + (response_body or b'')
            return response

        elif method == b'POST':
            with open(os.path.join(DIRECTORY_NAME, filename), 'wb') as f:
                f.write(body)
            logger.info(f'POST in {filename} successfully')
            response_headers = 'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n'.encode('utf-8')
            return response_headers

        elif method == b'OPTIONS':
            response_headers = 'HTTP/1.1 200 OK\r\nAllow: GET, POST, OPTIONS\r\nContent-Length: 0\r\n\r\n'.encode(
                'utf-8')
            return response_headers

        else:
            logger.warning(f'Method {method} is not allowed')
            response_headers = 'HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 0\r\n\r\n'.encode('utf-8')
            return response_headers

    else:
        logger.warning(f'Bad requests structure')
        response_headers = 'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n'.encode('utf-8')
        return response_headers


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    logger.info(f'Server listening on {HOST}:{PORT}')
    while True:
        user, addr = server.accept()
        with user:
            logger.info('Connected by', addr)
            request = user.recv(1024)
            response = handle_request(request)
            user.sendall(response)

# http://127.0.0.1:7000/main_page.html
"""
Пример GET запроса:
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n
Accept-Language: en-US,en;q=0.5\r\n
Accept-Encoding: gzip, deflate, br\r\n
Connection: keep-alive\r\n
Cookie: _ga=GA1.2.1234567890.1649508463; _gid=GA1.2.9876543210.1649508463\r\n
Upgrade-Insecure-Requests: 1\r\n
\r\n

POST
POST /submit-form HTTP/1.1\r\n
Host: example.com\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n
Accept-Language: en-US,en;q=0.5\r\n
Accept-Encoding: gzip, deflate, br\r\n
Connection: keep-alive\r\n
Cookie: _ga=GA1.2.1234567890.1649508463; _gid=GA1.2.9876543210.1649508463\r\n
Content-Type: application/x-www-form-urlencoded\r\n
Content-Length: 27\r\n
\r\n
username=john&password=doe\r\n

"""
