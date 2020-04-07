# flake8: noqa

from utils import stress

from fib_dict import dict_fibonacci
from fib_lru import lru_fibonacci
from fib_bmemcached import bmemcached_fibonacci
from fib_bmemcached import tls_bmemcached_fibonacci
from fib_pymemcache import pymemcache_fibonacci
from fib_pymemcache import tls_pymemcache_fibonacci

prefixes = [
    "dict",
    "lru",
    "bmemcached",
    "tls_bmemcached",
    "pymemcache",
    "tls_pymemcache",
]

stress(prefixes=prefixes, globals=globals())
