"""
Task Scheduler - Main Entry Point
(Linked list queue + linked list history + hash table chaining)

I wrote this in a simple, clean style suitable for a university project.
Each function now includes full documentation explaining purpose,
parameters, and return values.
"""
from task_scheduler import Scheduler

if __name__ == "__main__":
    # Define file path for saving/loading state
    filePath = "state_history/state_history.json"
    # Creating an object from the scheduler class
    scheduler = Scheduler(7)

    scheduler.submit_task(10)
    scheduler.submit_task(15)
    scheduler.submit_task(8)

    scheduler.show_hash()
    scheduler.show_queue()

    scheduler.run_next_task()
    scheduler.show_history()

    scheduler.save_to_file(filePath)

    new_scheduler = Scheduler(7)
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

