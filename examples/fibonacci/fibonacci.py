from functools import lru_cache
from oslo_cache import core as cache
from oslo_config import cfg

import timeit

dict_cache = {}

CONF = cfg.CONF

caching = cfg.BoolOpt("caching", default=True)
cache_time = cfg.IntOpt("cache_time", default=3600)
CONF.register_opts([caching, cache_time], "fibonacci")

cache.configure(CONF)
cache_region = cache.create_region()
MEMOIZE = cache.get_memoization_decorator(CONF, cache_region, "fibonacci")

CONF(["--config-file", f"{__file__.replace('.py', '.conf')}"])

cache.configure_cache_region(CONF, cache_region)


def validate_input(n):
    if type(n) != int:
        raise TypeError("n must be a positive int")
    if n < 1:
        raise ValueError("n must be a positive int")


def simple_fibonacci(n):
    validate_input(n)

    if n in (1, 2):
        return 1

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


@MEMOIZE
def oslo_fibonacci(n):
    validate_input(n)

    if n in (1, 2):
        return 1

    return lru_fibonacci(n - 1) + lru_fibonacci(n - 2)


if __name__ == "__main__":

    print("Cache warmup")
    for prefix in ["dict", "lru", "oslo"]:
        time = timeit.timeit(
            f"{prefix}_fibonacci(128);"
            f"{prefix}_fibonacci(256);"
            f"{prefix}_fibonacci(512);"
            f"{prefix}_fibonacci(1000)",
            globals=globals(),
            number=1,
        )

        print(f"{prefix}\t{time:.6f}")

    print("Cache stress")
    for prefix in ["dict", "lru", "oslo"]:
        time = timeit.timeit(
            f"{prefix}_fibonacci(1000)",
            globals=globals(),
            number=10000,
        )

        print(f"{prefix}\t{time:.6f}")
