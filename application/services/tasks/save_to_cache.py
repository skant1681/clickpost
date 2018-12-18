from application import celery
from pymemcache.client import base

#background task to save {awbno, status} in memcache
@celery.task(name='save_to_cache.save_to_memcache')
def save_to_memcache(awbno, status):
    _client = base.Client(('localhost', 11211))
    _client.set(awbno, status)
    return "Cache updated"