from random import randint
from math import floor, ceil

# theoretically, insertion sort is optimal for arrays of 12 or fewer elements
# merge sort prefers larger powers of 2
# therefore max run size is set to 8
MAX_RUN_SIZE = 8

def get_run_length(array):
    run_length = len(array)
    remainder = 0
    while run_length > MAX_RUN_SIZE:
        remainder = run_length % 2
        run_length = floor(run_length / 2)
    return run_length + remainder

def insertion_sort(array, start, end):
    for i in range(start, end):
        k = i        
        while k >= start and array[k] > array[k+1]:
            array[k], array[k+1] = array[k+1], array[k]
            k -= 1    

def merge(array, left, mid, right):
    final = []
    i = left
    k = mid
    while i < mid and k < right:
        if array[i] < array[k]:
            final.append(array[i])
            i += 1
            continue
        final.append(array[k])
        k += 1

    while i < mid:
        final.append(array[i])
        i += 1

    while k < right:
        final.append(array[k])
        k += 1

    # finally, swap with the in-place array elements
    for i in range(left, right):
        array[i] = final[i - left]

def timsort(array):
    run_length = get_run_length(array)
    for run_start in range(0,len(array),run_length):
        # select either the normal end or the end of the parent array
        run_end = min((run_start + run_length) - 1,len(array) - 1)        
        # unfortunately, we can't use slice syntax since this is in-place
        insertion_sort(array, run_start, run_end)
    merge_length = run_length
    while merge_length < len(array):
        for left in range(0, len(array), merge_length * 2):
            mid = left + merge_length
            right = min(len(array),mid + merge_length)
            if mid < right:
                merge(array,left,mid,right)
        merge_length *= 2

def frequency(array):
    freqs = {}
    for el in array:
        if el not in freqs:
            freqs[el] = 0
        freqs[el] += 1
    return freqs

def compare_frequencies(a, b):

    freq_a = frequency(a)
    freq_b = frequency(b)

    for k in freq_a:
        if k not in freq_b: return False
        if freq_a[k] != freq_b[k]: return False

    for k in freq_b:
        if k not in freq_a: return False
        if freq_a[k] != freq_b[k]: return False

    return True

def check_sorted(array):
    prev = array[0]
    for el in array:
        if el < prev:
            return False
        prev = el
    return True

def main():
    randlist = [randint(1,50) for i in range(50)]
    copy = randlist[:]
    print(randlist)
    timsort(randlist)
    print(randlist)
    print(f"Sorted: {check_sorted(randlist)}, Frequencies match: {compare_frequencies(randlist, copy)}")

if __name__ == "__main__":
    main()
