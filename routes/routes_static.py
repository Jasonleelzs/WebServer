from routes import current_user, login_required
from routes import http_response
from utils import template, log


def route_index(request):
    u = current_user(request)
    log('current user', u)
    body = template('index.html', username=u.username)
    return http_response(body)


def route_static(request):
    filename = request.query.get('file', 'd1.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_dict():
    r = {
        '/': login_required(route_index),
        '/static': login_required(route_static),
    }
    return r
