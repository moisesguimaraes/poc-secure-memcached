import utils

dict_cache = {}


def dict_fibonacci(n):
    utils.validate_input(n)

    if n in (1, 2):
        return 1

    if n not in dict_cache:
        dict_cache[n] = dict_fibonacci(n - 1) + dict_fibonacci(n - 2)

    return dict_cache[n]


if __name__ == "__main__":
    utils.stress(["dict"], globals=globals())
