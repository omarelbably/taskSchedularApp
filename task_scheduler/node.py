"""
Node Class Module
"""


class Node:
    """
    Node used for all linked list structures (queue and history).
    Stores a value and a pointer to the next node.
    """

    def __init__(self, value):
        """
        Purpose:
            Initialize a node that wraps a value for use in a linked list.

        Parameters:
            value: Any object to store inside the node.

        Returns:
            None
        """
        self.value = value
        self.next = None

