import time
from multiprocessing import Queue, Process
from random import randint


arr_100 = [randint(0, 9) for x in range(100)]
arr_1000 = [randint(0, 9) for x in range(1000)]
arr_10000 = [randint(0, 9) for x in range(10000)]


def get_execution_time(func):
  """Wrapper for getting function execution time"""
  def wrap(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    execution_time = end - start
    return (result, execution_time)
  return wrap


def bubble_sort(array):
  n = len(array)
  for i in range(n):
    for j in range(0, n - i - 1):
      if array[j] > array[j + 1]:
        array[j], array[j + 1] = array[j + 1], array[j]
  return array


@get_execution_time
def bubble_sort_with_time(array):
  return bubble_sort(array)


def bubble_sort_queue_handler(subarray, queue):
  sorted_subarray = bubble_sort(subarray)
  queue.put(sorted_subarray)


@get_execution_time
def multiproccess_sort(array, proccess_amount):
  subarray_length = len(array) // proccess_amount

  processes = []
  queues = []
  for i in range(proccess_amount):
    start_idx = i * subarray_length
    end_idx = start_idx + subarray_length
    if i == proccess_amount - 1:
      end_idx = None
    subarray = array[start_idx:end_idx]
    queue = Queue()
    proces = Process(target=bubble_sort_queue_handler, args=(array[start_idx:end_idx], queue))
    processes.append(proces)
    queues.append(queue)

  for proces in processes:
    proces.start()

  for proces in processes:
    proces.join()

  sorted_subarrays = []
  for queue in queues:
    sorted_subarray = queue.get()
    sorted_subarrays.extend(sorted_subarray)
  return sorted(sorted_subarrays)
  
# Wnioski:
# - dla 100 i 1000 elementowych tablic zwykle sortowanie babelkowe bylo najszybsze
# - dla 100 i 1000 elementowych tablic szybsze bylo wykonanie sortowania na 5 procesach niz na 10
# - wykonanie sortowania na 5 procesach 1000 elementowej tablicy jest delikatnie szybsze niz posortowanie na 5 procesach 100 elementowej tablicy
# - dla 10000 elementowej tablicy zwykle sortowanie babelkowe trwalo bardzo dlugo - 5 sekund
# - dla 10000 elementowej tablicy sortowanie na 10 procesach bylo dwa razy szybsze niz sortowanie na 5 procesach

if __name__ == '__main__':
  bubble_sort100_exec_time = bubble_sort_with_time(arr_100)[1]
  bubble_sort1000_exec_time = bubble_sort_with_time(arr_1000)[1]
  bubble_sort10000_exec_time = bubble_sort_with_time(arr_10000)[1]

  multiproccess_sort100_5_exec_time = multiproccess_sort(arr_100, 5)[1]
  multiproccess_sort100_10_exec_time = multiproccess_sort(arr_100, 10)[1]

  multiproccess_sort1000_5_exec_time = multiproccess_sort(arr_1000, 5)[1]
  multiproccess_sort1000_10_exec_time = multiproccess_sort(arr_1000, 10)[1]

  multiproccess_sort10000_5_exec_time = multiproccess_sort(arr_10000, 5)[1]
  multiproccess_sort10000_10_exec_time = multiproccess_sort(arr_10000, 10)[1]
  
  
  print(f'Sortowanie babelkowe tablicy 100 elementowej - czas wykonania: {bubble_sort100_exec_time}')
  print(f'Sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {bubble_sort1000_exec_time}')
  print(f'Sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {bubble_sort10000_exec_time}')
  print('----------------------------------')
  print(f'Wieloprocesowe(5) sortowanie babelkowe tablicy 100 elementowej - czas wykonania: {multiproccess_sort100_5_exec_time}')
  print(f'Wieloprocesowe(10) sortowanie babelkowe tablicy 100 elementowej - czas wykonania: {multiproccess_sort100_10_exec_time}')
  print('----------------------------------')
  print(f'Wieloprocesowe(5) sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {multiproccess_sort1000_5_exec_time}')
  print(f'Wieloprocesowe(10) sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {multiproccess_sort1000_10_exec_time}')
  print('----------------------------------')
  print(f'Wieloprocesowe(5) sortowanie babelkowe tablicy 10000 elementowej - czas wykonania: {multiproccess_sort10000_5_exec_time}')
  print(f'Wieloprocesowe(10) sortowanie babelkowe tablicy 10000 elementowej - czas wykonania: {multiproccess_sort10000_10_exec_time}')