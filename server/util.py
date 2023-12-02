from typing import Any, Collection, Optional, TypeVar

T = TypeVar('T')
V = TypeVar('V')

def remove_nulls(arr: list[T]) -> list[T]:
    return [i for i in arr if i]

def first_from_bulk(arr: list[tuple[Any, T]]) -> Optional[T]:
    return arr[0][1] if arr else None

def search_index(orig_arr: list[T], search: list[T]) -> list[tuple[int, int]]:
    # search for the index of each element in search in orig_arr
    # both lists must be sorted
    
    ptr_1 = 0
    ptr_2 = 0
    result: list[tuple[int, int]] = []
    while ptr_1 < len(orig_arr) and ptr_2 < len(search):
        if orig_arr[ptr_1] == search[ptr_2]:
            result.append((ptr_1, ptr_2))
            ptr_2 += 1
        ptr_1 += 1

    return result

def many_many_map(arr: Collection[tuple[T, V]]) -> dict[T, list[V]]:
    result: dict[T, list[V]] = {}
    for k, v in arr:
        if k not in result:
            result[k] = []
        result[k].append(v)
    return result

def not_none(x: Optional[T]) -> T:
    assert x is not None
    return x