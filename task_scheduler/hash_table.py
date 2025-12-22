"""
HashTable Class Module
"""


class HashTable:
    """
    Hash table that uses separate chaining to store queued jobs.
    Provides fast duplicate checking.
    """

    def __init__(self, size=53):
        """
        Purpose:
            Create a hash table with a fixed number of buckets.

        Parameters:
            size (int): Number of buckets (default 53).

        Returns:
            None
        """
        if size < 3:
            size = 3
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def hash(self, job_id):
        """
        Purpose:
            Compute the bucket index for a given job ID.

        Parameters:
            job_id (int)

        Returns:
            int: Index of the bucket.
        """
        return job_id % self.size

    def _extract_job(self, entry):
        """
        Internal helper to normalize stored entries to a Job object.
        The table may store either Job objects or Node objects (where
        entry.value is a Job).
        """
        # If the entry looks like a Node with a `value` attribute, return that
        if hasattr(entry, "value") and hasattr(entry.value, "job_id"):
            return entry.value
        # Otherwise assume it's a Job-like object
        return entry

    def insert(self, item):
        """
        Purpose:
            Insert a job or node into the hash table unless a duplicate exists.

        Parameters:
            item (Job or Node)

        Returns:
            None

        Raises:
            ValueError: If job ID already exists in the same bucket.
        """
        # Determine job id from the provided item
        job_obj = self._extract_job(item)
        job_id = job_obj.job_id

        idx = self.hash(job_id)
        bucket = self.buckets[idx]

        for e in bucket:
            existing = self._extract_job(e)
            if existing.job_id == job_id:
                raise ValueError("Duplicate job ID!")

        # Store the original item (so Nodes stay as Nodes, Jobs stay as Jobs)
        bucket.append(item)

    def search(self, job_id):
        """
        Purpose:
            Look up a job using its ID.

        Parameters:
            job_id (int)

        Returns:
            Job or None: The matching job from the bucket.
        """
        idx = self.hash(job_id)
        for e in self.buckets[idx]:
            existing = self._extract_job(e)
            if existing.job_id == job_id:
                return existing
        return None

    def remove(self, job_id):
        """
        Purpose:
            Remove a job from the hash table.

        Parameters:
            job_id (int)

        Returns:
            Job or None: The removed job, or None if not found.
        """
        idx = self.hash(job_id)
        bucket = self.buckets[idx]

        for i in range(len(bucket)):
            existing = self._extract_job(bucket[i])
            if existing.job_id == job_id:
                removed = bucket.pop(i)
                return self._extract_job(removed)

        return None
