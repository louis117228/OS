import threading
import time
import random

def timer_job():
    global timer_flag
    timer_flag = 0

def writer_job():
    global data, reader_num, write_counts, condition, lock, timer_flag
    while (timer_flag):
        while (reader_num > 0):
            condition.wait()
        
        with lock:
            data += 10
            write_counts += 1

            print('[', threading.currentThread().getName(), ']', ' enter critical section.', sep = '')
            print('[', threading.currentThread().getName(), ']', ' write data to ', data, '.', sep = '')
            sleep_time = random.randint(1,3)
            print('[', threading.currentThread().getName(), ']', ' sleep for ', sleep_time, ' seconds.', sep = '')
            for _ in range(sleep_time):
                print('[', threading.currentThread().getName(), ']', ' .', sep = '')
                time.sleep(0.5)
            print('[', threading.currentThread().getName(), ']', ' wake up~', sep = '')
            print('[', threading.currentThread().getName(), ']', ' exit critical section.', sep = '')

def reader_job():
    global data, reader_num, read_counts, condition, lock, timer_flag
    while (timer_flag):
        with lock:
            reader_num += 1
            read_counts += 1
        
        with condition:
            print('     [', threading.currentThread().getName(), ']', ' enter critical section.', sep = '')
            print('     [', threading.currentThread().getName(), ']', ' read data, data is ', data, '.', sep = '')
            sleep_time = random.randint(1,3)
            print('     [', threading.currentThread().getName(), ']', ' sleep for ', sleep_time, ' seconds.', sep = '')
            time.sleep(sleep_time)
            print('     [', threading.currentThread().getName(), ']', ' wake up~', sep = '')
            print('     [', threading.currentThread().getName(), ']', ' exit critical section.', sep = '')

        with lock:
            reader_num -= 1
            if (reader_num == 0):
                condition.notifyAll()
        
if __name__ == "__main__":
    # writer_num = input('how many writers?')
    # reader_num = input('how many readers?')
    print('first_reader_writer start')
    print('-------------------------')

    data = 0
    reader_num = 0
    write_counts = 0
    read_counts = 0
    lock = threading.Lock()
    condition = threading.Condition()
    timer_flag = 1
    timer = threading.Timer(15, timer_job)
    my_writer1 = threading.Thread(target = writer_job, name = 'writer1')
    my_writer2 = threading.Thread(target = writer_job, name = 'writer2')
    my_reader1 = threading.Thread(target = reader_job, name = 'reader1')
    my_reader2 = threading.Thread(target = reader_job, name = 'reader2')
    my_reader3 = threading.Thread(target = reader_job, name = 'reader3')
    my_reader4 = threading.Thread(target = reader_job, name = 'reader4')

    timer.start()
    my_writer1.start()
    my_writer2.start()
    my_reader1.start()
    my_reader2.start()
    my_reader3.start()
    my_reader4.start()

    my_writer1.join()
    my_writer2.join()
    my_reader1.join()
    my_reader2.join()
    my_reader3.join()
    my_reader4.join()
    timer.join()

    print('-------------------------')
    print('first_reader_writer end')
    print('total write_counts:',write_counts)
    print('total read_counts:',read_counts)
    print('Done.')