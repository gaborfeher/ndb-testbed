from flask import Flask
import logging
import random
import string
import time
import gc

app = Flask(__name__)

NEW_NDB = False
DISABLE_CACHE = False

if NEW_NDB:
    from google.cloud import ndb
    logging.getLogger('google.cloud.ndb').setLevel(logging.WARNING)
    def ndb_wsgi_middleware(wsgi_app):
        def middleware(environ, start_response):
            ndb_client = ndb.Client()
            if DISABLE_CACHE:
                global_cache = None
            else:
                global_cache = ndb.RedisCache.from_environment()
            with ndb_client.context(global_cache=global_cache) as context:
                if DISABLE_CACHE:
                    context.set_cache_policy(False)
                    context.set_memcache_policy(False)
                result = wsgi_app(environ, start_response)
                # gc.collect()  # (not needed in these tests, but sometimes needed) https://github.com/googleapis/python-ndb/issues/336
                return result
        return middleware
    app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)
else:
    from google.appengine.ext import ndb
    def ndb_wsgi_middleware(wsgi_app):
        def middleware(environ, start_response):
            if DISABLE_CACHE:
                context = ndb.get_context()
                context.set_cache_policy(False)
                context.set_memcache_policy(False)
            return wsgi_app(environ, start_response)
        return middleware
    app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)


class User(ndb.Model):
    name = ndb.StringProperty()

    @classmethod
    def parent_key(cls):
        return ndb.Key('SomeData', 'default')

class SubData(ndb.Model):
    str0 = ndb.StringProperty()
    int0 = ndb.IntegerProperty()
    int1 = ndb.IntegerProperty()
    int2 = ndb.IntegerProperty()
    int3 = ndb.IntegerProperty()
    int4 = ndb.IntegerProperty()

class SomeData(ndb.Model):
    prop0 = ndb.StringProperty()
    prop1 = ndb.StringProperty()
    prop2 = ndb.StringProperty()
    prop3 = ndb.StringProperty()
    prop4 = ndb.StringProperty()
    prop5 = ndb.StringProperty()
    prop6 = ndb.StringProperty()
    prop7 = ndb.StringProperty()
    prop8 = ndb.StringProperty()
    flag = ndb.BooleanProperty()
    items = ndb.StructuredProperty(SubData, repeated=True)

    @classmethod
    def parent_key(cls):
        return ndb.Key('SomeData', 'default')


@app.route('/init')
def init():
    random.seed(123)
    randstr = lambda: ''.join(random.choice(string.lowercase) for _ in range(30))
    for _ in range(10):
        items = []
        for _ in range(40):
            item = SomeData(
                prop0=randstr(),
                prop1=randstr(),
                prop2=randstr(),
                prop3=randstr(),
                prop4=randstr(),
                prop6=randstr(),
                prop7=randstr(),
                prop8=randstr(),
                flag=random.randint(1, 2) == 1,
                items=[
                    SubData(str0=randstr(),
                    int0=random.randint(1, 2000),
                    int1=random.randint(1, 2000),
                    int2=random.randint(1, 2000),
                    int3=random.randint(1, 2000),
                    int4=random.randint(1, 2000)) for _ in range(30)
                ],
                parent=SomeData.parent_key())
            items.append(item)
        ndb.put_multi(items)
    return 'ok'

def _query0():
    return SomeData.query(SomeData.flag == True, ancestor=SomeData.parent_key())

@app.route('/test1')
def test1():
    t1 = time.time()
    count = _query0().count()
    t2 = time.time()
    return 'cnt= {}, time= {}'.format(count, t2-t1)


@app.route('/test2')
def test2():
    t1 = time.time()
    items = _query0().order(SomeData.prop0).fetch(projection=[
        SomeData.prop0,
        SomeData.prop1,
        SomeData.prop2,
        SomeData.prop3,
        SomeData.prop4])
    count = len(items)
    t2 = time.time()
    return 'cnt= {}, time= {}'.format(count, t2-t1)


@app.route('/cleanup')
def cleanup():
    keys = SomeData.query().fetch(keys_only=True)
    ndb.delete_multi(keys)
    return 'ok'


@app.route('/list')
def list():
    return '<br>'.join(str(d) for d in SomeData.query())


@app.route('/')
def main():
    return 'ok'

