import time
import matplotlib.pyplot as plt
from multiprocessing import Queue, Process
from heap_merge import merge_sorted_arrays
from random import randint

arr_100 = [randint(0, 99) for _ in range(100)]
arr_1000 = [randint(0, 99) for _ in range(1000)]
arr_10000 = [randint(0, 99) for _ in range(10000)]

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
def multiprocess_sort(array, process_amount):
  subarray_length = len(array) // process_amount

  processes = []
  queues = []
  for i in range(process_amount):
    start_idx = i * subarray_length
    end_idx = start_idx + subarray_length
    if i == process_amount - 1:
      end_idx = None
    subarray = array[start_idx:end_idx]
    queue = Queue()
    proces = Process(target=bubble_sort_queue_handler, args=(subarray, queue))
    processes.append(proces)
    queues.append(queue)

  for proces in processes:
    proces.start()

  for proces in processes:
    proces.join()

  sorted_subarrays = []
  for queue in queues:
    sorted_subarray = queue.get()
    sorted_subarrays.append(sorted_subarray)
  return merge_sorted_arrays(sorted_subarrays)


def show_diagram(title, x_label, y_label, x_data, y_data):
  plt.plot(x_data, y_data, marker='o')
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.title(title)
  plt.grid(True)
  plt.show()


def bubble_sort_diagram(exec_time100, exec_time1000, exec_time10000):
  array_lengths = [100, 1000, 10000]
  exec_times = [exec_time100, exec_time1000, exec_time10000]
  show_diagram('Bubble sort execution time vs. array length', 'Array length', 'Execution time', array_lengths, exec_times)


def multiprocess_sort_diagram(arr_length, exec_time2, exec_time5, exec_time10):
  num_of_processes = [2, 5, 10]
  exec_times = [exec_time2, exec_time5, exec_time10]
  show_diagram(f'{arr_length} elements array multiprocess sort execution time vs. number of processes', 'Number of processes', 'Execution time', num_of_processes, exec_times)


if __name__ == '__main__':
  bubble_sort100_exec_time = bubble_sort_with_time(arr_100)[1]
  print(f'Sortowanie babelkowe tablicy 100 elementowej - czas wykonania: {bubble_sort100_exec_time}')

  bubble_sort1000_exec_time = bubble_sort_with_time(arr_1000)[1]
  print(f'Sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {bubble_sort1000_exec_time}')

  bubble_sort10000_exec_time = bubble_sort_with_time(arr_10000)[1]
  print(f'Sortowanie babelkowe tablicy 10000 elementowej - czas wykonania: {bubble_sort10000_exec_time}')

  bubble_sort_diagram(bubble_sort100_exec_time, bubble_sort1000_exec_time, bubble_sort10000_exec_time) 
  print('----------------------------------')

  multiprocess_sort100_2_exec_time = multiprocess_sort(arr_100, 2)[1]
  print(f'Wieloprocesowe(2) sortowanie babelkowe tablicy 100 elementowej - czas wykonania: {multiprocess_sort100_2_exec_time}')

  multiprocess_sort100_5_exec_time = multiprocess_sort(arr_100, 3)[1]
  print(f'Wieloprocesowe(5) sortowanie babelkowe tablicy 100 elementowej - czas wykonania: {multiprocess_sort100_5_exec_time}')

  multiprocess_sort100_10_exec_time = multiprocess_sort(arr_100, 4)[1]
  print(f'Wieloprocesowe(10) sortowanie babelkowe tablicy 100 elementowej - czas wykonania: {multiprocess_sort100_10_exec_time}')

  multiprocess_sort_diagram(100, multiprocess_sort100_2_exec_time, multiprocess_sort100_5_exec_time, multiprocess_sort100_10_exec_time)  
  print('----------------------------------')

  multiprocess_sort1000_2_exec_time = multiprocess_sort(arr_1000, 2)[1]
  print(f'Wieloprocesowe(2) sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {multiprocess_sort1000_2_exec_time}')

  multiprocess_sort1000_5_exec_time = multiprocess_sort(arr_1000, 3)[1]
  print(f'Wieloprocesowe(5) sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {multiprocess_sort1000_5_exec_time}')

  multiprocess_sort1000_10_exec_time = multiprocess_sort(arr_1000, 4)[1]
  print(f'Wieloprocesowe(10) sortowanie babelkowe tablicy 1000 elementowej - czas wykonania: {multiprocess_sort1000_10_exec_time}')

  multiprocess_sort_diagram(1000, multiprocess_sort1000_2_exec_time, multiprocess_sort1000_5_exec_time, multiprocess_sort1000_10_exec_time)  
  print('----------------------------------')

  multiprocess_sort10000_2_exec_time = multiprocess_sort(arr_10000, 3)[1]
  print(f'Wieloprocesowe(2) sortowanie babelkowe tablicy 10000 elementowej - czas wykonania: {multiprocess_sort10000_2_exec_time}')

  multiprocess_sort10000_5_exec_time = multiprocess_sort(arr_10000, 4)[1]
  print(f'Wieloprocesowe(5) sortowanie babelkowe tablicy 10000 elementowej - czas wykonania: {multiprocess_sort10000_5_exec_time}')

  multiprocess_sort10000_10_exec_time = multiprocess_sort(arr_10000, 5)[1]
  print(f'Wieloprocesowe(10) sortowanie babelkowe tablicy 10000 elementowej - czas wykonania: {multiprocess_sort10000_10_exec_time}')
  

  multiprocess_sort_diagram(10000, multiprocess_sort10000_2_exec_time, multiprocess_sort10000_5_exec_time, multiprocess_sort10000_10_exec_time)


# Obserwacje w większości przypadków na naszych komputerach:
# 1. zwykle sortowanie babelkowe jest najszybsze dla tablic 100 i 1000 elementowych
# 2. czas wykonania wieloprocesowego sortowanie babelkowego dla malych tablic(100n, 1000n) wzrasta wraz ze wzrostem liczby procesow
# 3. czas wykonania sortowania na 3 i 4 procesach jest szybsze dla tablicy 1000 elementowej niz dla tablicy 100 elementowej
# 4. sortowanie tablicy 10000 elementowej najszybsze bylo wykonujac je na 4 procesach 