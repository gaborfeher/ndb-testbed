from flask import Flask
from google.cloud import ndb
import logging
import json
import os
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
# import grpc
# ndb._retry.TRANSIENT_CODES += (grpc.StatusCode.ABORTED,)


def ndb_wsgi_middleware(wsgi_app):
    ndb_client = ndb.Client()
    def middleware(environ, start_response):
        with ndb_client.context(global_cache=None) as context:
            context.set_cache_policy(False)
            # The issue can also be reproduced with caching, but it's a bit
            # simpler and maybe faster this way.
            return wsgi_app(environ, start_response)
    return middleware
app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)


class ProductCopy5(ndb.Model):
    s = ndb.StringProperty()
    b1 = ndb.BooleanProperty()
    b2 = ndb.BooleanProperty()
    b3 = ndb.BooleanProperty()
    b4 = ndb.BooleanProperty()
    i = ndb.IntegerProperty(repeated=True)

    @classmethod
    def query_for_test(cls):
        return cls.query(
            cls.b1 == True,
            cls.b2 == False,
            cls.b3 == True,
            cls.b4 == False,
            cls.i == 1,
            ancestor=cls.parent_key())

    @staticmethod
    def parent_key(name = 'default'):
        return ndb.Key('ProductCopy5', name)


@app.route('/test')
def test5():
    def keys(prods):
        return [p.key for p in prods]
    def ids(keys):
        return [k.id() for k in keys]
    logging.getLogger('google.cloud.ndb').setLevel(logging.DEBUG)
    ko = ProductCopy5.query_for_test().fetch(keys_only=True)
    pro = ProductCopy5.query_for_test().fetch(projection=[ProductCopy5.s])
    logging.getLogger('google.cloud.ndb').setLevel(logging.WARNING)
    return f'''The following two lists should contain the same ids:<br>
{ids(ko)} == {ids(keys(pro))}'''


@app.route('/init/<int:offset>')
def init(offset):
    path = os.path.dirname(os.path.abspath(__file__)) + '/export.json'
    with open(path, 'r') as f:
        data = json.load(f)
    k = offset + 1
    to_put = []
    for entry in data[offset:]:
        pc5 = ProductCopy5(
            key=ndb.Key('ProductCopy5', 'default', 'ProductCopy5', k),
            s='hello',
            b1=entry['b1'],
            b2=entry['b2'],
            b3=entry['b3'],
            b4=entry['b4'],
            i=entry['i'])
        to_put.append(pc5)
        k += 1
        if len(to_put) >= 100:
            ndb.put_multi(to_put)
            logging.info(f'saved until {to_put[-1].key.id()}')
            to_put = []
    if len(to_put) > 0:
        ndb.put_multi(to_put)
        logging.info(f'saved until {to_put[-1].key.id()}')

    return 'ok'


@app.route('/cleanup')
def cleanup():
    ks = ProductCopy5.query().fetch(keys_only=True)
    ndb.delete_multi(ks)
    return 'ok'


@app.route('/')
def main():
    return 'ok'

