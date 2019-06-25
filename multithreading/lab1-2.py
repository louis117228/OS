import numpy as np
import threading
import multiprocessing
import time

thread_result = [[],[],[],[]]

def thread_func(thread_result, row, sub_matA, matB):
    thread_result[row] = np.matmul(sub_matA, matB)

def process_func(result_queue, row, sub_matA, matB):
    result_queue_pair = (row, np.matmul(sub_matA, matB))
    result_queue.put(result_queue_pair)

def main():
    # Generate random matrix and result matrix
    matA = np.random.randint(10, size = (100, 100))
    matB = np.random.randint(10, size = (100, 100))

    # print(matA)
    # print(matB)
    
    # # method1
    start_time = time.time()
    result = np.zeros((matA.shape[0], matB.shape[1]))
    for row in range(0, matA.shape[0]):
        result[row] = np.matmul(matA[row], matB)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(result)
    print("elapsed_time1:",elapsed_time,sep='')
    # # Compare with numpy's multiplication result
    # print('Answer is correct:', np.all(np.matmul(matA, matB) == result))

    # # method2
    start_time = time.time()
    # How many thread you want to use
    thread_num = 4
    threads = []

    # split the matA with num_base(close to average)
    num_base = matA.shape[0]//4
    if matA.shape[0]%4==0:
        sub_matA = [ matA[0:num_base], \
        matA[num_base:2*num_base], \
        matA[2*num_base:3*num_base], \
        matA[3*num_base:4*num_base] ]
    elif matA.shape[0]%4==1:
        sub_matA = [ matA[0:num_base+1], \
        matA[num_base+1:2*num_base+1], \
        matA[2*num_base+1:3*num_base+1], \
        matA[3*num_base+1:4*num_base+1] ]
    elif matA.shape[0]%4==2:
        sub_matA = [ matA[0:num_base+1], \
        matA[num_base+1:2*num_base+2], \
        matA[2*num_base+2:3*num_base+2], \
        matA[3*num_base+2:4*num_base+2] ]
    elif matA.shape[0]%4==3:
        sub_matA = [ matA[0:num_base+1], \
        matA[num_base+1:2*num_base+2], \
        matA[2*num_base+2:3*num_base+3], \
        matA[3*num_base+3:4*num_base+3] ]
    
    # Assign job to threads
    for row in range(thread_num):
        # Pass argument to function with tuple
        thread = threading.Thread(target = thread_func, args = (thread_result, row, sub_matA, matB))
        threads.append(thread)

    # run all threads
    for thread in threads:
        thread.start()

    # Wait for threads finish
    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(thread_result)
    print("elapsed_time2:",elapsed_time,sep='')

    # # method3
    start_time = time.time()

    result_queue = multiprocessing.Manager().Queue()

    process_num = 4
    jobs = []
    
    process_result = [[],[],[],[]]

    # split the matA with num_base(close to average)
    num_base = matA.shape[0]//4
    if matA.shape[0]%4==0:
        sub_matA = [ matA[0:num_base], \
        matA[num_base:2*num_base], \
        matA[2*num_base:3*num_base], \
        matA[3*num_base:4*num_base] ]
    elif matA.shape[0]%4==1:
        sub_matA = [ matA[0:num_base+1], \
        matA[num_base+1:2*num_base+1], \
        matA[2*num_base+1:3*num_base+1], \
        matA[3*num_base+1:4*num_base+1] ]
    elif matA.shape[0]%4==2:
        sub_matA = [ matA[0:num_base+1], \
        matA[num_base+1:2*num_base+2], \
        matA[2*num_base+2:3*num_base+2], \
        matA[3*num_base+2:4*num_base+2] ]
    elif matA.shape[0]%4==3:
        sub_matA = [ matA[0:num_base+1], \
        matA[num_base+1:2*num_base+2], \
        matA[2*num_base+2:3*num_base+3], \
        matA[3*num_base+3:4*num_base+3] ]

    for row in range(process_num):
        process = multiprocessing.Process(target = process_func, args = (result_queue, row, sub_matA, matB))
        jobs.append(process)

    for process in jobs:
        process.start()

    for process in jobs:
        process.join()

    while not result_queue.empty():
        process_result_pair = result_queue.get()
        process_result[process_result_pair[0]] = process_result_pair[1]
        
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(process_result)
    print("elapsed_time3:",elapsed_time,sep='')

if __name__ == "__main__":
    main()