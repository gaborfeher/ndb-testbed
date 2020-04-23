from flask import Flask
from google.cloud import ndb
import logging
import sys


logging.basicConfig(
    format='[%(levelname)s] %(name)s: %(message)s',
    level=logging.INFO)
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
h1 = logging.StreamHandler(sys.stderr)
h1.setFormatter(logging.Formatter('%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s'))
app.logger.addHandler(h1)


logging.getLogger('google.cloud.ndb').setLevel(logging.WARNING)


def ndb_wsgi_middleware(wsgi_app):
    ndb_client = ndb.Client()
    def middleware(environ, start_response):
        with ndb_client.context(global_cache=None) as context:
            context.set_cache_policy(False)
            return wsgi_app(environ, start_response)
    return middleware
app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)


@app.route('/demo')
def demo():
    class EmptyStuff(ndb.Model):
        pass

    ndb.put_multi(
        EmptyStuff(key=ndb.Key('EmptyStuff', i+1))
        for i in range(1100))

    q = EmptyStuff.query()
    findings = [
        (i, q.fetch(limit=1, offset=i)[0].key.id())
        for i in range(995, 1006)
    ]
    return str(findings) + '\n'


@app.route('/')
def main():
    return 'ok'

