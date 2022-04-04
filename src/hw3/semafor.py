import threading


class SimpleSemaphore:
    """
    Semaphore primitive.

    It manages an internal counter, which is decremented on acquire call
    and increased on each release call. An attempt to go below zero will block
    the calling thread, until some other thread releases the semaphore.

    if _is_bounded == True, then if counter exceeds initial capacity a
    ValueError is raised in release.
    """

    def __init__(self, capacity: int = 1, is_bounded: bool = False):
        """
        :param capacity: initial capacity of a semaphore, number of threads who can acquire the semaphore
        at the same time.
        :param is_bounded: whether this semaphore is bounded, if it is, then on exceeding initial capacity,
        ValueError will be raised.
        """
        self._capacity: int = capacity
        self._currentValue: int = self._capacity
        self._lock: threading.Lock = threading.Lock()
        self._condition: threading.Condition = threading.Condition(self._lock)
        self._is_bounded: bool = is_bounded

    def acquire(self):
        """
        Acquire the semaphore, decreases the internal counter by 1.
        If the current counter value is 0, then the calling thread is blocked, until
        some other thread that acquired the semaphore releases it.
        """
        self._lock.acquire()
        while not self._currentValue:
            self._condition.wait()
        self._currentValue -= 1
        self._lock.release()

    def release(self, n: int = 1):
        """
        Release the semaphore, increases the internal counter value by n.
        If counter value was zero, and other threads were waiting for semaphore to be released,
        then this method releases n of those threads.

        :raises ValueError if semaphore is bounded and counter value exceeded the initial capacity
        """
        with self._lock:
            self._condition.notify(n)
            self._currentValue += n
            if self._is_bounded and self._currentValue > self._capacity:
                raise ValueError("Counter exceeded upper bound")

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
