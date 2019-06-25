import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir, queue_buffer):
    # Search sub-dir in top_dir and put them in queue
    queue_buffer.put(top_dir)
    for f_path in os.listdir(path = top_dir):
        join_path = os.path.join(top_dir, f_path)
        if (os.path.isdir(join_path)):
            producer(join_path, queue_buffer)

def consumer(queue_buffer):
    global file_count
    # search file in directory
    try:
        top_dir = queue_buffer.get(timeout = 1)
        for f_path in os.listdir(path = top_dir):
            join_path = os.path.join(top_dir, f_path)
            if (os.path.isfile(join_path)):
                lock.acquire()
                file_count += 1
                lock.release()
    except:
        return

def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 20
    consumers = []
    for _ in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()