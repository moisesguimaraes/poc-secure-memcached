import bmemcached
import ssl
import utils

# without TLS

client = bmemcached.Client(("localhost:11211",))
client.flush_all()

# with TLS

ctx = ssl.create_default_context(cafile="tls/ca-root.crt")

# uncomment for client auth
# ctr.load_cert_chain("tls/client.crt", "tls/client.key")

tls_client = bmemcached.Client(("localhost:11212",), tls_context=ctx)
tls_client.flush_all()


def bmemcached_fibonacci(n):
    utils.validate_input(n)

    if n in (1, 2):
        return 1

    f = client.get(str(n))
    if f is None:
        f = bmemcached_fibonacci(n - 1) + bmemcached_fibonacci(n - 2)
        client.set(str(n), str(f))

    return int(f)


def tls_bmemcached_fibonacci(n):
    utils.validate_input(n)

    if n in (1, 2):
        return 1

    f = tls_client.get(str(n))
    if f is None:
        f = tls_bmemcached_fibonacci(n - 1) + tls_bmemcached_fibonacci(n - 2)
        tls_client.set(str(n), str(f))

    return int(f)


if __name__ == "__main__":
    utils.stress(["bmemcached", "tls_bmemcached"], globals=globals())
