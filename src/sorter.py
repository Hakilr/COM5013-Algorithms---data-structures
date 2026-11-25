"""Sorting algorithms: bubble sort, merge sort, quick sort and counting sort.

Every function takes a list (or any iterable) and an optional `key` function that
says what to compare, for example key=lambda card: card.difficulty. Each returns a
new sorted list and leaves the input unchanged.

              best         average      worst        extra memory   stable
bubble sort   O(n)         O(n^2)       O(n^2)       O(1)           yes
merge sort    O(n log n)   O(n log n)   O(n log n)   O(n)           yes
quick sort    O(n log n)   O(n log n)   O(n^2)*      O(log n)       no
counting sort O(n + k)     O(n + k)     O(n + k)     O(n + k)       yes

*  with the "first" pivot on already-sorted data. The default pivot avoids that case.
   k is the number of possible key values.
"""


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


# ---------------------------------------------------------------------------
# Quick sort
# ---------------------------------------------------------------------------

PIVOT_RULES = ("median_of_three", "first")


def quick_sort(items, key=_identity, pivot="median_of_three"):
    """Return a new sorted list using in-place quick sort (Hoare partition).

    A pivot value is chosen and the items are rearranged so that everything in
    the left part is no larger than the pivot and everything in the right part is
    no smaller. Each part is then sorted the same way.

    pivot chooses how the pivot is picked:
      "median_of_three" (default): the median of the first, middle and last items.
          Already-sorted and reverse-sorted data are no longer bad cases.
      "first": the first item. Simple, but already-sorted data splits as unevenly
          as possible every time, giving O(n^2). It is here so the worst case can
          be benchmarked.

    Average O(n log n). Worst case O(n^2). Not stable: swapping moves equal items
    past each other. Many equal keys are not a problem (both scans stop at equal
    items, so the parts stay balanced). Extra memory is O(log n), because the code
    always recurses into the smaller part and loops over the larger one, so the
    recursion can never get deep, even in the worst case.
    """
    if pivot not in PIVOT_RULES:
        raise ValueError(f"pivot must be one of {PIVOT_RULES}, not {pivot!r}")
    result = list(items)
    _quick_sort_range(result, 0, len(result) - 1, key, pivot)
    return result


def _quick_sort_range(items, low, high, key, pivot):
    """Sort items[low..high] in place."""
    while low < high:
        # Move the chosen pivot to the front of the range. Having it there is what
        # guarantees that both parts below are smaller than the whole range.
        chosen = _choose_pivot(items, low, high, key, pivot)
        items[low], items[chosen] = items[chosen], items[low]
        pivot_key = key(items[low])

        # Hoare partition: i moves right until it finds an item that belongs on
        # the right, j moves left until it finds one that belongs on the left, and
        # the two are swapped. They stop when they meet or cross.
        i, j = low - 1, high + 1
        while True:
            i += 1
            while key(items[i]) < pivot_key:
                i += 1
            j -= 1
            while key(items[j]) > pivot_key:
                j -= 1
            if i >= j:
                break
            items[i], items[j] = items[j], items[i]

        # items[low..j] are <= the pivot and items[j+1..high] are >= the pivot.
        # Recurse into the smaller part and loop over the larger one, so the
        # recursion depth is at most log2(n).
        if j - low + 1 <= high - j:
            _quick_sort_range(items, low, j, key, pivot)
            low = j + 1
        else:
            _quick_sort_range(items, j + 1, high, key, pivot)
            high = j


def _choose_pivot(items, low, high, key, rule):
    """Return the index of the pivot for items[low..high]."""
    if rule == "first":
        return low
    middle = (low + high) // 2
    a, b, c = key(items[low]), key(items[middle]), key(items[high])
    if a < b:
        if b < c:
            return middle
        return high if a < c else low
    if a < c:
        return low
    return high if b < c else middle


# ---------------------------------------------------------------------------
# Counting sort
# ---------------------------------------------------------------------------

MAX_RANGE = 10_000_000   # refuse key ranges larger than this (the counts list would be huge)


def counting_sort(items, key, smallest, largest):
    """Return a new list sorted by an integer key between smallest and largest.

    It counts how many items have each key value, turns the counts into starting
    positions, then drops each item straight into place. Nothing is compared with
    anything else, so it is not limited by the O(n log n) bound of comparison sorts.

    Time and extra memory are O(n + k), where k = largest - smallest + 1. That is
    excellent when k is small (difficulty has k = 3) and poor when k is far larger
    than n. Stable: items are placed in their original order.

    Raises TypeError if a key is not an integer, and ValueError if a key falls
    outside smallest..largest or the range is invalid or larger than MAX_RANGE.
    """
    if smallest > largest:
        raise ValueError("smallest must not be larger than largest")
    size = largest - smallest + 1
    if size > MAX_RANGE:
        raise ValueError(
            f"key range of {size:,} is too large for counting sort (limit {MAX_RANGE:,})"
        )

    items = list(items)
    keys = [key(item) for item in items]          # call key once per item

    counts = [0] * size
    for k in keys:
        if not isinstance(k, int):
            raise TypeError(f"counting sort needs integer keys, got {k!r}")
        if k < smallest or k > largest:           # a negative index would silently wrap around
            raise ValueError(f"key {k} is outside the range {smallest} to {largest}")
        counts[k - smallest] += 1

    start = [0] * size                            # where each key's block begins
    for i in range(1, size):
        start[i] = start[i - 1] + counts[i - 1]

    result = [None] * len(items)
    for item, k in zip(items, keys):              # original order, so ties stay in order
        slot = k - smallest
        result[start[slot]] = item
        start[slot] += 1
    return result
