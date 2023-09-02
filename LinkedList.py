class Node:
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        """ Checks if the doubly linked list is empty"""
        return self.head is None

    def prepend(self, data):
        """Inserts a node with the given data value at the beginning of the list"""
        if not self.is_empty():
            node = Node(data, None, self.head)
            self.head.prev = node
            self.head = node
        else:
            node = Node(data, None, None)
            self.head = self.tail = node

    def append(self, data):
        """Inserts a node with the given data value at the end of the list"""
        if not self.is_empty():
            node = Node(data, self.tail, None)
            self.tail.next = node
            self.tail = node
        else:
            node = Node(data, None, None)
            self.head = self.tail = node

    def insert_after(self, target_data, data):
        """Inserts a node with the given data value after the node containing target data"""
        n = self.head
        while not n.data == target_data:
            if n == self.tail:
                raise ValueError("Data is not in double linked list")
            n = n.next
        node = Node(data, n, n.next)
        n.next.prev = node
        n.next = node

    def insert_before(self, target_data, data):
        """Inserts a node with the given data value before the node containing target data"""
        n = self.head
        while not n.data == target_data:
            if n == self.tail:
                raise ValueError("Data is not in double linked list")
            n = n.next
        node = Node(data, n.prev, n)
        n.prev.next = node
        n.prev = node

    def delete(self, data):
        """Removes the node containing the given data value from the list"""
        n = self.head
        while n.data != data:
            if n == self.tail:
                raise ValueError("Data is not in double linked list")
            n = n.next
        n.next.prev = n.prev
        n.prev.next = n.next

    def display(self):
        """Displays the elements of the doubly linked list"""
        n = self.head
        while n.next is not None:
            print(n.data, end=' ')
            n = n.next
        print(self.tail.data)

try:
    ll = LinkedList()
    ll.append(15)
    ll.append(20)
    ll.prepend(10)
    ll.insert_before(20, 18)
    ll.insert_after(10, 12)
    ll.delete(12)
    ll.display()
except ValueError as ve:
    print(str(ve))
