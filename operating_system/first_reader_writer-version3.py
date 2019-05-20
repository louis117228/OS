import threading
import time
import random

# -----------------------------------------------------------------------------
# Python Cookbook by David Ascher, Alex Martelli
# Allowing Multithreaded Read Access While Maintaining a Write Lock
# Credit: Sami Hangaslammi
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s04.html
class ReadWriteLock:
    """ A lock object that allows many simultaneous "read locks", but
    only one "write lock." """

    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire()
        try:
            self._readers += 1
        finally:
            self._read_ready.release()

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        """ Release a write lock. """
        self._read_ready.release()
# -----------------------------------------------------------------------------

def timer_job():
    global timer_flag
    timer_flag = 0

class Writer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global data, write_counts, rw_lock, timer_flag
        while (timer_flag):
            rw_lock.acquire_write()
            data += 10
            write_counts += 1
            print('[', self.name, ']', ' enter critical section.', sep = '')
            print('[', self.name, ']', ' write data to ', data, '.', sep = '')
            sleep_time = random.randint(1,5)
            print('[', self.name, ']', ' sleep for ', sleep_time/2, ' seconds.', sep = '')
            for _ in range(sleep_time):
                print('[', self.name, ']', ' .', sep = '')
                time.sleep(0.5)
            print('[', self.name, ']', ' wake up~', sep = '')
            print('[', self.name, ']', ' exit critical section.', sep = '')
            rw_lock.release_write()
            
class Reader(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global data, read_counts, rw_lock, lock, timer_flag
        while (timer_flag):
            rw_lock.acquire_read()
            with lock:
                # many readers may let race condition happen, so it need a lock
                read_counts += 1
            print('     [', self.name, ']', ' enter critical section.', sep = '')
            print('     [', self.name, ']', ' read data, data is ', data, '.', sep = '')
            sleep_time = random.randint(1,5)
            print('     [', self.name, ']', ' sleep for ', sleep_time, ' seconds.', sep = '')
            time.sleep(sleep_time)
            print('     [', self.name, ']', ' wake up~', sep = '')
            print('     [', self.name, ']', ' exit critical section.', sep = '')
            rw_lock.release_read()

if __name__ == "__main__":
    # writer_num = input('how many writers?')
    # reader_num = input('how many readers?')
    print('first_reader_writer start')
    print('-------------------------')

    data = 0
    reader_num = 0
    write_counts = 0
    read_counts = 0
    rw_lock = ReadWriteLock()
    lock = threading.Lock()
    timer_flag = 1
    timer = threading.Timer(120, timer_job)
    my_writer1 = Writer(name = 'writer1')
    my_writer2 = Writer(name = 'writer2')
    my_reader1 = Reader(name = 'reader1')
    my_reader2 = Reader(name = 'reader2')
    my_reader3 = Reader(name = 'reader3')
    my_reader4 = Reader(name = 'reader4')

    timer.start()
    my_writer1.start()
    my_writer2.start()
    my_reader1.start()
    my_reader2.start()
    my_reader3.start()

    my_writer1.join()
    my_writer2.join()
    my_reader1.join()
    my_reader2.join()
    my_reader3.join()
    timer.join()

    print('-------------------------')
    print('first_reader_writer end')
    print('total write_counts:',write_counts)
    print('total read_counts:',read_counts)
    print('Done.')