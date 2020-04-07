import utils

from functools import lru_cache


@lru_cache()
def lru_fibonacci(n):
    utils.validate_input(n)

    if n in (1, 2):
        return 1

    return lru_fibonacci(n - 1) + lru_fibonacci(n - 2)


if __name__ == "__main__":
    utils.stress(["lru"], globals=globals())
