class MinHeap:
    """A binary min-heap stored in a list.

    The smallest item is always at index 0. For the item at index i, its
    children are at 2i + 1 and 2i + 2, and its parent is at (i - 1) // 2.

    push: O(log n)   pop: O(log n)   peek: O(1)   build from n items: O(n)
    """

    def __init__(self, items=None):
        self._items = list(items) if items else []
        # Bottom-up heapify: sift down every non-leaf node. This is O(n), which
        # is faster than pushing n items one at a time (O(n log n)).
        for i in range(len(self._items) // 2 - 1, -1, -1):
            self._sift_down(i)

    def __len__(self):
        return len(self._items)

    def push(self, item):
        """Add an item, then move it up until its parent is not larger."""
        self._items.append(item)
        self._sift_up(len(self._items) - 1)

    def peek(self):
        """Return the smallest item without removing it."""
        if not self._items:
            raise IndexError("peek from an empty heap")
        return self._items[0]

    def pop(self):
        """Remove and return the smallest item."""
        if not self._items:
            raise IndexError("pop from an empty heap")
        smallest = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last      # move the last item to the root...
            self._sift_down(0)         # ...then sink it to its correct place
        return smallest

    def is_valid(self):
        """Check the heap property (every parent <= its children). Used in tests."""
        items = self._items
        return all(items[(i - 1) // 2] <= items[i] for i in range(1, len(items)))

    def _sift_up(self, index):
        items = self._items
        item = items[index]
        while index > 0:
            parent = (index - 1) // 2
            if items[parent] <= item:
                break
            items[index] = items[parent]   # pull the larger parent down
            index = parent
        items[index] = item

    def _sift_down(self, index):
        items = self._items
        size = len(items)
        item = items[index]
        while True:
            child = 2 * index + 1
            if child >= size:
                break
            if child + 1 < size and items[child + 1] < items[child]:
                child += 1                  # pick the smaller of the two children
            if items[child] >= item:
                break
            items[index] = items[child]     # pull the smaller child up
            index = child
        items[index] = item