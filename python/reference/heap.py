from math import floor

def left(idx : int):
    return 2*idx

def right(idx : int):
    return 2*idx + 1

def parent(idx : int):
    return (idx-1) / 2

def swap(arr, i1, i2):
    temp = arr[i1]
    arr[i1] = arr[i2]
    arr[i2] = temp

def max_heapify(arr : list[int], idx : int, heap_size : int):
    largest = idx
    lc = left(idx)
    rc = right(idx)

    if lc <= heap_size and arr[lc] > arr[largest]:
        largest = lc

    if rc <= heap_size and arr[rc] > arr[largest]:
        largest = rc
    
    if largest != idx:
        swap(arr, idx, largest)
        max_heapify(arr, largest, heap_size)

def build_max_heap(arr : list[int]):
    heap_size = len(arr)

    for i in range( floor(heap_size / 2) - 1, -1, -1):
        max_heapify(arr, i, heap_size)

arr = [1,2,3,4,5,6]

build_max_heap(arr)

print(arr)