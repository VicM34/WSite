from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as parse
import os


class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""
        # Убираем параметры запроса, если они есть
        path = self.path.split('?')[0]

        # Маршрутизация
        if path == '/static/css/custom.css':
            self.serve_static_file('static/css/custom.css', 'text/css')
        elif path == '/':
            self.serve_html_file('templates/index.html')
        elif path == '/catalog':
            self.serve_html_file('templates/catalog.html')
        elif path == '/category':
            self.serve_html_file('templates/category.html')
        elif path == '/contacts':
            self.serve_html_file('templates/contacts.html')
        else:
            # По заданию: все GET-запросы возвращают страницу контактов
            self.serve_html_file('templates/contacts.html')

    def do_POST(self):
        """Обработка POST-запросов (дополнительное задание)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Парсим данные
        parsed_data = parse.parse_qs(post_data.decode('utf-8'))

        # Выводим в консоль
        print("=" * 50)
        print("Получены данные формы:")
        for key, value in parsed_data.items():
            print(f"{key}: {value[0] if value else ''}")
        print("=" * 50)

        # Возвращаем страницу контактов
        self.serve_html_file('templates/contacts.html')

    def serve_html_file(self, filepath):
        """Отправка HTML-файла"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(404, f"File {filepath} not found")

    def serve_static_file(self, filepath, content_type):
        """Отправка статических файлов"""
        try:
            with open(filepath, 'rb') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, f"File {filepath} not found")


def run_server():
    """Запуск сервера"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print('Сервер запущен на http://localhost:8000')
    print('Нажмите Ctrl+C для остановки')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nСервер остановлен')
        httpd.server_close()


if __name__ == '__main__':
    run_server()