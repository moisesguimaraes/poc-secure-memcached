import ssl
import utils

from pymemcache.client.base import Client

# without TLS

client = Client(("localhost", 11211))
client.flush_all()

# with TLS

ctx = ssl.create_default_context(cafile="tls/ca-root.crt")

# uncomment for client auth
# ctr.load_cert_chain("tls/client.crt", "tls/client.key")

tls_client = Client(("localhost", 11212), tls_context=ctx)
tls_client.flush_all()


def pymemcache_fibonacci(n):
    utils.validate_input(n)

    if n in (1, 2):
        return 1

    f = client.get("p"+str(n))
    if f is None:
        f = pymemcache_fibonacci(n - 1) + pymemcache_fibonacci(n - 2)
        client.set("p"+str(n), str(f))

    return int(f)


def tls_pymemcache_fibonacci(n):
    utils.validate_input(n)

    if n in (1, 2):
        return 1

    f = tls_client.get(str(n))
    if f is None:
        f = tls_pymemcache_fibonacci(n - 1) + tls_pymemcache_fibonacci(n - 2)
        tls_client.set(str(n), str(f))

    return int(f)


if __name__ == "__main__":
    utils.stress(["pymemcache", "tls_pymemcache"], globals=globals())
