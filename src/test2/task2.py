import multiprocessing
import random


def partition(array, low, high):
    """
    return index m such that start <= m < end, and swap elements in
    array so that array[start, m-1] <= array[m] <= array[m+1, end]
    """
    pivot = array[high]

    i = low - 1

    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1

            (array[i], array[j]) = (array[j], array[i])

    (array[i + 1], array[high]) = (array[high], array[i + 1])

    return i + 1


def quicksort(array, start, end, numproc=1):
    """
    sort array[start, end] using numproc processes
    """
    assert numproc >= 1, "At least one process is required!"
    if start >= end:
        return
    m = partition(array, start, end)
    if numproc > 1:
        left = multiprocessing.Process(target=quicksort, args=(array, start, m - 1, numproc // 2))
        left.start()
        quicksort(array, m + 1, end, numproc - numproc // 2)
        left.join()
    else:
        quicksort(array, start, m - 1)
        quicksort(array, m + 1, end)


if __name__ == '__main__':
    array = [random.randint(0, 10) for i in range(10)]
    quicksort(array, 0, len(array) - 1, 2)
    print(array)
