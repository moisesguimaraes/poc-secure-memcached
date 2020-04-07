# flake8: noqa

from utils import stress

from fib_dict import dict_fibonacci
from fib_lru import lru_fibonacci
from fib_bmemcached import bmemcached_fibonacci
from fib_bmemcached import tls_bmemcached_fibonacci

stress(["dict", "lru", "bmemcached", "tls_bmemcached"], globals=globals())
