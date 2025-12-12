"""
Job Class Module
"""

from datetime import datetime


class Job:
    """
    Represents a single job in the system.
    Stores its ID, submission time, status, and execution timestamp.
    """

    def __init__(self, job_id):
        """
        Purpose:
            Create a new job with a unique ID and record its submission time.

        Parameters:
            job_id (int): The ID of the job submitted by the user.

        Returns:
            None
        """
        self.job_id = job_id
        self.submit_timestamp = datetime.now()
        self.status = "queued"
        self.execution_timestamp = None

    def to_dict(self):
        """
        Purpose:
            Convert this Job object to a dictionary for JSON serialization.

        Parameters:
            None

        Returns:
            dict: Contains job ID, submission time, status, and execution time.
        """
        return {
            "job_id": self.job_id,
            "submit_timestamp": self.submit_timestamp.isoformat(),
            "status": self.status,
            "execution_timestamp": self.execution_timestamp.isoformat()
                if self.execution_timestamp else None
        }

    @staticmethod
    def from_dict(d):
        """
        Purpose:
            Restore a Job object from a dictionary created using to_dict().

        Parameters:
            d (dict): Dictionary containing job information.

        Returns:
            Job: A fully restored Job object.
        """
        j = Job(int(d["job_id"]))
        j.submit_timestamp = datetime.fromisoformat(d["submit_timestamp"])
        j.status = d["status"]
        if d["execution_timestamp"]:
            j.execution_timestamp = datetime.fromisoformat(d["execution_timestamp"])
        return j

