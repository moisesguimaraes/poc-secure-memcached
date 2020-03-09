import ssl
import timeit

from functools import lru_cache

import bmemcached

dict_cache = {}

# without TLS

client = bmemcached.Client(("localhost:11211", ))
client.flush_all()

# with TLS

ctx = ssl.create_default_context(cafile="certs/gen/crt/ca-root.crt")

# uncomment for client auth
# ctr.load_cert_chain("certs/gen/crt/client.crt", "certs/gen/key/client.key")

tls_client = bmemcached.Client(("localhost:11212", ), tls_context=ctx)
tls_client.flush_all()


def validate_input(n):
    if type(n) != int:
        raise TypeError("n must be a positive int")
    if n < 1:
        raise ValueError("n must be a positive int")


def simple_fibonacci(n, show_me_the_real_deal=False):
    validate_input(n)

    if n in (1, 2):
        return 1

    if n > 30 and not show_me_the_real_deal:
        # just for it not to take forever...
        raise RecursionError("that is too much man!")

    return simple_fibonacci(n - 1) + simple_fibonacci(n - 2)


def dict_fibonacci(n):
    validate_input(n)

    if n in (1, 2):
        return 1

    if n not in dict_cache:
        dict_cache[n] = dict_fibonacci(n - 1) + dict_fibonacci(n - 2)

    return dict_cache[n]


@lru_cache()
def lru_fibonacci(n):
    validate_input(n)

    if n in (1, 2):
        return 1

    return lru_fibonacci(n - 1) + lru_fibonacci(n - 2)


def bmemcached_fibonacci(n):
    validate_input(n)

    if n in (1, 2):
        return 1

    f = client.get(str(n))
    if f is None:
        f = bmemcached_fibonacci(n - 1) + bmemcached_fibonacci(n - 2)
        client.set(str(n), str(f))

    return int(f)


def tls_bmemcached_fibonacci(n):
    validate_input(n)

    if n in (1, 2):
        return 1

    f = tls_client.get(str(n))
    if f is None:
        f = tls_bmemcached_fibonacci(n - 1) + tls_bmemcached_fibonacci(n - 2)
        tls_client.set(str(n), str(f))

    return int(f)


if __name__ == "__main__":

    print("Cache warmup")
    for prefix in ["dict", "lru", "bmemcached", "tls_bmemcached"]:
        time = timeit.timeit(
            f"{prefix}_fibonacci(128);"
            f"{prefix}_fibonacci(256);"
            f"{prefix}_fibonacci(512);"
            f"{prefix}_fibonacci(1000)",
            globals=globals(),
            number=1,
        )

        print(f"{prefix}\t{time:.6f}")

    times = 1000
    print(f"Cache stress {times} times")
    for prefix in ["dict", "lru", "bmemcached", "tls_bmemcached"]:
        time = timeit.timeit(
            f"{prefix}_fibonacci(1000)",
            globals=globals(),
            number=times,
        )

        print(f"{prefix}\t{time:.6f}")
