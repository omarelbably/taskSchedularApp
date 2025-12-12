"""
LinkedQueue Class Module
"""

from .node import Node


class LinkedQueue:
    """
    A simple linked list implementation of a FIFO queue.
    Used to store waiting/queued jobs.
    """

    def __init__(self):
        """
        Purpose:
            Create an empty queue with head and tail pointers.

        Parameters:
            None

        Returns:
            None
        """
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, value):
        """
        Purpose:
            Add a job to the end of the queue.

        Parameters:
            value (Job): The job to insert.

        Returns:
            None
        """
        new_node = Node(value)
        if self.head is None:  # First element
            self.head = new_node
            self.tail = new_node
        else:  # Append to end
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        """
        Purpose:
            Remove and return the job at the front of the queue.

        Parameters:
            None

        Returns:
            Job or None: The oldest queued job, or None if empty.
        """
        if self.head is None:
            print("Queue is empty!")
            return None

        value = self.head.value
        self.head = self.head.next

        if self.head is None:
            print("Queue is now empty after dequeue.")
            self.tail = None

        print("Dequeued job:", value.job_id)
        self.size -= 1
        return value

    def peek(self):
        """
        Purpose:
            Return the first job in the queue without removing it.

        Parameters:
            None

        Returns:
            Job or None: The first job, or None if queue empty.
        """
        if self.head is None:
            print("Queue is empty! Nothing to peek.")
            return None
        print("Peeked job:", self.head.value.job_id)
        return self.head.value

    def is_empty(self):
        """
        Purpose:
            Check whether the queue is empty.

        Parameters:
            None

        Returns:
            bool: True if queue is empty, otherwise False.
        """
        return self.size == 0

    def to_list(self):
        """
        Purpose:
            Convert all queue nodes into a list of Job objects.

        Parameters:
            None

        Returns:
            list[Job]: List of all jobs currently in the queue.
        """
        out = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

