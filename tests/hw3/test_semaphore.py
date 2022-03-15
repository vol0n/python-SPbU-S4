import pytest
import threading as th
import time
from src.hw3.semafor import SimpleSemaphore


def test_one_thread_no_deadlock():
    d: dict = {}
    with SimpleSemaphore():
        d["one"] = 1

    assert "one" in d


def test_two_threads_no_deadlock():
    shared_dict: dict = {"a": 0}

    def foo():
        with SimpleSemaphore():
            shared_dict["a"] += 1

    threads = [th.Thread(target=foo, args=()) for _ in range(2)]
    for thr in threads:
        thr.start()

    threads[0].join()
    threads[1].join()

    assert shared_dict["a"] == 2


@pytest.mark.parametrize("k, total_number_of_threads", [(2, 3), (3, 3), (4, 10)])
def test_only_k_threads_enter(k, total_number_of_threads):
    """
    check that SimpleSemaphore allows to enter the critical section only to k
    threads, with total_number_of_threads >= k trying to enter the section
    """
    barrier = True
    sem = SimpleSemaphore(capacity=k)
    entered_fun = [False] * total_number_of_threads
    entered_cs = [False] * total_number_of_threads

    def fun(thread_idx: int):
        entered_fun[thread_idx] = True
        with sem:
            entered_cs[thread_idx] = True
            while barrier:
                time.sleep(0.01)
        # entered_cs[thread_idx] = False

    threads = [th.Thread(target=fun, args=(i,)) for i in range(total_number_of_threads)]
    for thr in threads:
        thr.start()

    # wait until all threads are run
    while not all(entered_fun):
        time.sleep(0.01)

    # check that only two threads have entered the critical section
    assert sum(entered_cs) == k

    # release the threads cycling inside critical section
    barrier = False


def test_bounded_semaphore_raises():
    with pytest.raises(ValueError):
        semaphore = SimpleSemaphore(capacity=2, is_bounded=True)
        semaphore.release()
