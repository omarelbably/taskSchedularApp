"""
HistoryList Class Module
"""

from .node import Node


class HistoryList:
    """
    Stores all executed jobs in the order they were completed.
    Uses a singly linked list similar to the queue.
    """

    def __init__(self):
        """
        Purpose:
            Initialize an empty history list.

        Parameters:
            None

        Returns:
            None
        """
        self.head = None
        self.tail = None

    def add_to_history(self, job):
        """
        Purpose:
            Append an executed job to the history list.

        Parameters:
            job (Job): A job that has finished execution.

        Returns:
            Node: The node that was created and appended to the history list.
        """
        node = Node(job)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        return node

    def display_history(self):
        """
        Purpose:
            Convert the history linked list into a list of Job objects.

        Parameters:
            None

        Returns:
            list[Job]: Jobs in executed order.
        """
        arr = []
        cur = self.head
        while cur:
            arr.append(cur.value)
            cur = cur.next
        return arr

    def get_last_n(self, n):
        """
        Purpose:
            Return the last n executed jobs.

        Parameters:
            n (int): Number of most recent jobs to retrieve.

        Returns:
            list[Job]: List of up to n jobs. Can be empty.
        """
        if n <= 0:
            return []

        all_jobs = self.display_history()
        total = len(all_jobs)

        if total == 0:
            print("History is empty.")
            return []

        start_index = max(0, total - n)
        return all_jobs[start_index:]
