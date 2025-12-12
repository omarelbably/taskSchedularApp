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

    def insert(self, job):
        """
        Purpose:
            Insert a job into the hash table unless a duplicate exists.

        Parameters:
            job (Job)

        Returns:
            None

        Raises:
            ValueError: If job ID already exists in the same bucket.
        """
        idx = self.hash(job.job_id)
        bucket = self.buckets[idx]

        for j in bucket:
            if j.job_id == job.job_id:
                raise ValueError("Duplicate job ID!")

        bucket.append(job)

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
        for j in self.buckets[idx]:
            if j.job_id == job_id:
                return j
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
            if bucket[i].job_id == job_id:
                return bucket.pop(i)

        return None

