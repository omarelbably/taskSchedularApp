"""
Scheduler Class Module
"""

from datetime import datetime
import json

from .job import Job
from .linked_queue import LinkedQueue
from .history_list import HistoryList
from .hash_table import HashTable


class Scheduler:
    """
    Main system that manages job submission, execution,
    queueing, history tracking, and file saving/loading.
    """

    def __init__(self, hash_size=53):
        """
        Purpose:
            Set up the scheduler with a queue, hash table, and history list.

        Parameters:
            hash_size (int): Bucket count for hash table.

        Returns:
            None
        """
        self.queue = LinkedQueue()
        self.hash = HashTable(hash_size)
        self.history = HistoryList()
        self.executed_ids = set()

    def submit_task(self, job_id):
        """
        Purpose:
            Add a job to the queue if it is not already queued or executed.

        Parameters:
            job_id (int)

        Returns:
            Job: The newly created job.

        Raises:
            ValueError: If the job is duplicated.
        """
        if self.hash.search(job_id) is not None:
            raise ValueError("This job already exists in queue.")

        if job_id in self.executed_ids:
            raise ValueError("Job already executed earlier.")

        job = Job(job_id)
        self.queue.enqueue(job)
        self.hash.insert(job)
        return job

    def find_job(self, job_id):
        """
        Purpose:
            Locate a job in either the queue or the history list.

        Parameters:
            job_id (int)

        Returns:
            tuple or None:
                ("queue", Job) if found in queue
                ("history", Job) if found in history
                None if not found
        """
        j = self.hash.search(job_id)
        if j:
            return ("queue", j)

        if job_id in self.executed_ids:
            for x in self.history.display_history():
                if x.job_id == job_id:
                    return ("history", x)

        return None

    def run_next_task(self):
        """
        Purpose:
            Execute the next job in the queue.

        Parameters:
            None

        Returns:
            Job or None: The executed job, or None if queue empty.
        """
        if self.queue.is_empty():
            print("No tasks in queue.")
            return None

        job = self.queue.dequeue()
        self.hash.remove(job.job_id)

        print("Executing job:", job.job_id)
        job.status = "executed"
        job.execution_timestamp = datetime.now()

        self.history.add_to_history(job)
        self.executed_ids.add(job.job_id)

        return job

    def run_all(self):
        """
        Purpose:
            Execute all queued tasks in FIFO order.

        Parameters:
            None

        Returns:
            list[Job]: All executed jobs.
        """
        executed = []
        while not self.queue.is_empty():
            job = self.run_next_task()
            if job:
                executed.append(job)
        return executed

    def save_to_file(self, filename):
        """
        Purpose:
            Save queue and history data into a JSON file.

        Parameters:
            filename (str)

        Returns:
            None
        """
        data = {
            "queue": [job.to_dict() for job in self.queue.to_list()],
            "history": [job.to_dict() for job in self.history.display_history()]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print("Saved to", filename)

    def load_from_file(self, filename):
        """
        Purpose:
            Restore scheduler task_scheduler from a previously saved JSON file.

        Parameters:
            filename (str)

        Returns:
            None
        """
        with open(filename) as f:
            data = json.load(f)

        # Reset everything
        self.queue = LinkedQueue()
        self.hash = HashTable(self.hash.size)
        self.history = HistoryList()
        self.executed_ids = set()

        # Load queue
        for d in data.get("queue", []):
            job = Job.from_dict(d)
            self.queue.enqueue(job)
            self.hash.insert(job)

        # Load history
        for d in data.get("history", []):
            job = Job.from_dict(d)
            self.history.add_to_history(job)
            self.executed_ids.add(job.job_id)

        print("Loaded from", filename)

    # Debug helpers
    def show_queue(self):
        """Print all queued jobs in readable format."""
        print("Queue:")
        lst = self.queue.to_list()
        if not lst:
            print("  (empty)")
        for j in lst:
            print(" ", j.job_id, j.status)

    def show_history(self):
        """Print executed jobs with timestamps."""
        print("History:")
        for j in self.history.display_history():
            print(" ", j.job_id, j.status, j.execution_timestamp)

    def show_hash(self):
        """Print the hash table buckets and stored job IDs."""
        print("Hash table:")
        for i, bucket in enumerate(self.hash.buckets):
            ids = [j.job_id for j in bucket]
            print(i, ":", ids)

