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
        global data, write_counts, rw_lock, timer_flag, ready_condition, ready_queue
        while (timer_flag):
            with ready_condition:
                while (ready_queue[0] != self.name):
                    ready_condition.wait()

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

            with ready_condition:
                # print(ready_queue[0])
                del ready_queue[0]
                ready_queue.append(threading.current_thread().getName())
                ready_condition.notifyAll()
            
class Reader(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global data, read_counts, rw_lock, lock, timer_flag, ready_condition, ready_queue
        while (timer_flag):
            with ready_condition:
                while (ready_queue[0][0:5] not in self.name):
                    ready_condition.wait()

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
            
            with ready_condition:
                # print(ready_queue[ready_queue.index(self.name)])
                del ready_queue[ready_queue.index(self.name)]
                ready_queue.append(threading.current_thread().getName())
                ready_condition.notifyAll()

if __name__ == "__main__":
    writer_num = int(input('how many writers? '))
    reader_num = int(input('how many readers? '))
    print('first_reader_writer start')
    print('-------------------------')

    data = 0
    write_counts = 0
    read_counts = 0
    rw_lock = ReadWriteLock()
    lock = threading.Lock()
    timer_flag = 1 # if timer is up to 120 seconds, then flag will be 0 to end the jobs of writers and readers
    timer = threading.Timer(120, timer_job)
    writer_list = []
    reader_list = []
    ready_condition = threading.Condition()
    ready_queue = []
    for i in range(writer_num):
        i += 1 # let name start from 1
        my_writer = Writer(name = 'writer%d' % i)
        writer_list.append(my_writer)
        ready_queue.append(my_writer.getName())
    for i in range(reader_num):
        i += 1 # let name start from 1
        my_reader = Reader(name = 'reader%d' % i)
        reader_list.append(my_reader)
        ready_queue.append(my_reader.getName())

    timer.start()
    for i in range(writer_num):
        writer_list[i].start()
    for i in range(reader_num):
        reader_list[i].start()

    for i in range(writer_num):
        writer_list[i].join()
    for i in range(reader_num):
        reader_list[i].join()
    timer.join()

    print('-------------------------')
    print('first_reader_writer end')
    print('total write_counts:',write_counts)
    print('total read_counts:',read_counts)
    print('Done.')