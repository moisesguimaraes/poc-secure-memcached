import timeit


def validate_input(n):
    if type(n) != int:
        raise TypeError("n must be a positive int")
    if n < 1:
        raise ValueError("n must be a positive int")


def stress(prefixes=[], globals=None):
    print("Cache warmup with fib(128), fib(256), fib(512), fib(1000)")
    for prefix in prefixes:
        time = timeit.timeit(
            f"{prefix}_fibonacci(128);"
            f"{prefix}_fibonacci(256);"
            f"{prefix}_fibonacci(512);"
            f"{prefix}_fibonacci(1000)",
            globals=globals,
            number=1,
        )

        print(f"{prefix}\t{time:.6f}")

    times = 1000
    print(f"Cache stress with fib(1000) {times} times")
    for prefix in prefixes:
        time = timeit.timeit(
            f"{prefix}_fibonacci(1000)", globals=globals, number=times,
        )

        print(f"{prefix}\t{time:.6f}")
