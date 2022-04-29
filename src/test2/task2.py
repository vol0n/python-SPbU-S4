import multiprocessing
import random


def partition(array, start, end):
    """
    return index m such that start <= m < end, and swap elements in
    array so that array[start, m-1] <= array[m] <= array[m+1, end]
    """
    k = random.randint(start, end)
    x = array[k]
    array[start], array[k] = array[k], array[start]
    i = start
    j = end
    while True:
        while array[i] < x:
            i += 1
        while array[j] > x:
            j -= 1
        if i >= j:
            break
        array[i], array[j] = array[j], array[i]
        i += 1
        j -= 1
    return j


def quicksort(array, start, end, numproc=1):
    """
    sort array[start, end] using numproc processes
    """
    assert numproc >= 1, "At least one process is required!"
    if start >= end:
        return
    m = partition(array, start, end)
    if numproc > 1:
        left = multiprocessing.Process(target=quicksort, args=(array, start, m, numproc // 2))
        left.start()
        quicksort(array, m + 1, end, numproc - numproc // 2)
        left.join()
    else:
        quicksort(array, start, m)
        quicksort(array, m+1, end)


if __name__ == '__main__':
    array = [random.randint(0, 10) for i in range(10)]
    quicksort(array, 0, len(array)-1, 2)
    print(array)