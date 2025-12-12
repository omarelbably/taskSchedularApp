"""
TaskSchedulerApp - Main runnable class to orchestrate demo/usage
without modifying the underlying single-responsibility classes.
"""

from .scheduler import Scheduler


class TaskSchedulerApp:
    """
    Provides a simple executable wrapper around Scheduler to demonstrate
    submitting, executing, persisting, and reloading tasks.
    """

    def __init__(self, hash_size=7, state_path="state_history/state_history.json"):
        self.hash_size = hash_size
        self.state_path = state_path

    def run_demo(self):
        """Replicate the demo flow from main.py using a class interface."""
        filePath = self.state_path
        scheduler = Scheduler(self.hash_size)

        scheduler.submit_task(10)
        scheduler.submit_task(15)
        scheduler.submit_task(8)

        scheduler.show_hash()
        scheduler.show_queue()

        scheduler.run_next_task()
        scheduler.show_history()

        scheduler.save_to_file(filePath)

        new_scheduler = Scheduler(self.hash_size)
        new_scheduler.load_from_file(filePath)
        new_scheduler.show_queue()
        new_scheduler.show_history()

        scheduler.submit_task(101)
        scheduler.submit_task(112)
        scheduler.submit_task(80)
        scheduler.show_hash()
        scheduler.show_queue()
        scheduler.run_next_task()
        scheduler.show_history()
        scheduler.save_to_file(filePath)

        new_scheduler.load_from_file(filePath)
        new_scheduler.show_queue()
        new_scheduler.show_history()

