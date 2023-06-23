import heapq


def merge_sorted_arrays(arrays):
    heap = []
    merged = []

    for i, array in enumerate(arrays):
        if len(array) > 0:
            heapq.heappush(heap, (array[0], i, 0))

    while heap:
        value, array_index, element_index = heapq.heappop(heap)
        merged.append(value)

        if element_index + 1 < len(arrays[array_index]):
            next_element = arrays[array_index][element_index + 1]
            heapq.heappush(heap, (next_element, array_index, element_index + 1))

    return merged
