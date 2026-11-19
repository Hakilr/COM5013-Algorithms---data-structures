def _identity(item):
    return item


def bubble_sort(items, key=_identity):
    """Return a new sorted list using bubble sort.

    Best case O(n) (already sorted, thanks to the early exit), average and worst
    case O(n^2). Stable, and needs no extra memory beyond the copy.
    """
    result = list(items)
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if key(result[i]) > key(result[i + 1]):
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        if not swapped:      # a full pass with no swaps means the list is sorted
            break
    return result


def merge_sort(items, key=_identity):
    """Return a new sorted list using merge sort.

    O(n log n) in every case. Stable, but needs O(n) extra memory for merging.
    """
    items = list(items)
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    left = merge_sort(items[:middle], key)
    right = merge_sort(items[middle:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    """Merge two sorted lists into one sorted list."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Take from the right only if it is strictly smaller. On a tie the left
        # item goes first, which keeps equal items in their original order (stable).
        if key(right[j]) < key(left[i]):
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged