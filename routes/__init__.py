from models.session import Session
from models.todo import Todo
from utils import log
from models.user import User

import random

session = {}


def random_str():
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('sid', '')
    sessions = Session.all()
    for s in sessions:
        if s.session_id == session_id:
            u = User.find_by(id=s.user_id)
            return u
    return None


def response_with_headers(headers=None, status_code=200):
    header = 'HTTP/1.1 {} OK\r\nContent-Type: text/html\r\n'
    header = header.format(status_code)
    if headers is not None:
        header += ''.join([
            '{}: {}\r\n'.format(k, v) for k, v in headers.items()
        ])
    return header


def redirect(location, headers=None):
    h = {
        'Location': location
    }
    if headers is not None:
        h.update(headers)
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    log('redirect r', r)
    return r.encode()


def login_required(route_function):

    def f(request):
        u = current_user(request)
        if u is None:
            log('非登录用户')
            return redirect('/login')
        else:
            return route_function(request)

    return f


def error(request, code=404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def http_response(body, headers=None):
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


