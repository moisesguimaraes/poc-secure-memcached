import timeit
import utils


def no_cache_fibonacci(n):
    utils.validate_input(n)

    if n in (1, 2):
        return 1

    if n > 30:
        n = 30  # just for it not to take forever...

    return no_cache_fibonacci(n - 1) + no_cache_fibonacci(n - 2)


if __name__ == "__main__":
    for i in 1, 5, 10, 20, 30:
        time = timeit.timeit(
            f"no_cache_fibonacci({i})", globals=globals(), number=1,
        )
        print(f"no_cache({i})\t{time:.6f}")
