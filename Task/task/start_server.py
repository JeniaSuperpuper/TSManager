
import os



ip = 'localhost'
port = 8000

os.system(f'daphne -p {port} -b {ip} -v {3} task.asgi:application')