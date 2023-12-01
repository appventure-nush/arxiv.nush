from typing import TypeVar

T = TypeVar('T')

def remove_nulls(arr: list[T]) -> list[T]:
    return [i for i in arr if i]