import random

def generate_list(length : int, min : int = 1, max : int = 10000):
    return [random.randint(min,max) for i in range(length)]

def swap(arr, i1, i2):
    tmp = arr[i1]
    arr[i1] = arr[i2]
    arr[i2] = tmp

def lomuto_partition(arr, lower, upper):
    # let pivot be the far-right value
    pivot = arr[upper]
    # let i start to the left of lower (so that on increment it's at lower)
    i = lower - 1

    # for everything between indexes lower and upper
    # if something is less than pivot
    #   then put it in the next available left-hand slot (pointed by i)
    for j in range(lower, upper):
        if (arr[j] < pivot):
            i += 1
            swap(arr, i, j)

    # swap pivot with whatever's pointed by i (the next left hand slot) 
    swap(arr, i+1, upper)
    # return position of pivot
    return i+1

def hoares_partition(arr, lower, upper):
    pivot = arr[lower]
    # i.e. to the left of the lower bound
    i = lower - 1
    # i.e. to the right of the upper bound
    j = upper + 1

    # Basically, move the left and right pointers towards each other, swapping numbers in the wrong place
    # The goal is to place all numbers smaller than the pivot to the left of it
    while (True):

        # Find first element >= pivot
        i += 1
        while (arr[i] < pivot):
            i += 1
        
        # Find last element <= pivot
        j -= 1
        while (arr[j] > pivot):
            j -= 1

        # If they're at the same position, we found the pivot!
        if (i >= j):
            return j

        swap(arr, i, j)

def quicksort(arr, lower, upper, hoares = True):
    # choose the appropriate partition scheme based on input
    partition_fn = hoares_partition if hoares else lomuto_partition

    if lower < upper:
        # sort and find the pivot point of the partition
        pivot_i = partition_fn(arr, lower, upper)

        # hoares and lomuto take slightly different parameters; adjust left upper bound for the different schemes
        next_upper = pivot_i if hoares else pivot_i - 1

        # sort left of pivot
        quicksort(arr, lower, next_upper, hoares)

        # sort right of pivot
        quicksort(arr, pivot_i + 1, upper, hoares)

def main():
    arr = generate_list(10, 1, 10)
    print(f'Unsorted: {arr}')
    quicksort(arr, 0, len(arr) - 1, True)
    print(f'Sorted: {arr}')


if __name__ == "__main__":
    main()