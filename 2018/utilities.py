"""AoC Utilities"""


def print_(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{prefix}{result}")

        return result

    return wrapper
