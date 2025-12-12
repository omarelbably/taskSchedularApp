# Task Scheduler

A simple task scheduling system implemented in Python using linked lists and hash tables. This project demonstrates fundamental data structures including FIFO queues, linked lists, and hash tables with separate chaining.

## Features

- **Job Submission**: Submit jobs with unique IDs to the scheduling queue
- **FIFO Execution**: Jobs are executed in First-In-First-Out order
- **Duplicate Detection**: Hash table prevents duplicate job submissions
- **Execution History**: Track all executed jobs with timestamps
- **State Persistence**: Save and load scheduler state to/from JSON files

## Project Structure

```
taskSchedularApp/
├── .idea/
│   └── (IDE configuration files)
├── state_history/
│   └── (history/state files)
├── task_scheduler/
│   ├── __init__.py
│   ├── job.py
│   ├── node.py
│   ├── linked_queue.py
│   ├── history_list.py
│   ├── hash_table.py
│   └── scheduler.py
├── tests/
│   └── (test files)
├── Data Structure project 1 report.pdf
├── README.md
└── main.py

```
Explanation

.idea/ – IDE settings (likely from PyCharm or VS Code)

state_history/ – Stores runtime state/history outputs

task_scheduler/ – Core Python package with scheduler implementation

tests/ – Unit tests

main.py – Main runner script

README.md – Project documentation

PDF report – A report likely for a class/project

## Classes Overview

### Job
Represents a single job in the system with:
- `job_id`: Unique identifier
- `submit_timestamp`: When the job was submitted
- `status`: Current status ("queued" or "executed")
- `execution_timestamp`: When the job was executed (if applicable)

### Node
A generic linked list node used by both `LinkedQueue` and `HistoryList`.

### LinkedQueue
A FIFO queue implementation using a singly linked list:
- `enqueue(job)`: Add a job to the end of the queue
- `dequeue()`: Remove and return the job at the front
- `peek()`: View the front job without removing it
- `is_empty()`: Check if the queue is empty

### HistoryList
Stores executed jobs in completion order:
- `add_to_history(job)`: Add an executed job
- `display_history()`: Get all executed jobs as a list
- `get_last_n(n)`: Get the last n executed jobs

### HashTable
Hash table with separate chaining for fast duplicate detection:
- `insert(job)`: Insert a job (raises error if duplicate)
- `search(job_id)`: Find a job by ID
- `remove(job_id)`: Remove a job by ID

### Scheduler
Main controller that orchestrates all components:
- `submit_task(job_id)`: Submit a new job
- `run_next_task()`: Execute the next job in queue
- `run_all()`: Execute all queued jobs
- `find_job(job_id)`: Locate a job in queue or history
- `save_to_file(filename)`: Save state to JSON
- `load_from_file(filename)`: Load state from JSON

## Usage

### Basic Example

```python
from task_scheduler import Scheduler

# Create a scheduler with hash table size of 7
s = Scheduler(7)

# Submit jobs
s.submit_task(10)
s.submit_task(15)
s.submit_task(8)

# View current state
s.show_queue()
s.show_hash()

# Execute next job
s.run_next_task()

# View execution history
s.show_history()

# Save state to file
s.save_to_file("state_history/task_scheduler.json")

# Load state from file
new_scheduler = Scheduler(7)
new_scheduler.load_from_file("state_history/task_scheduler.json")
```

### Running the Demo

```powershell
python .\main.py
```

## Testing

Unit tests cover insertion, searching, dequeueing, and collision handling. To run them:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## State and Exports

- A dedicated package `state/` exists to host output state artifacts in the future.
- The exported scheduler state JSON is included under `state_history/state_history.json`.

## State File Format

The scheduler state is saved in JSON format:

```json
{
  "queue": [
    {
      "job_id": 8,
      "submit_timestamp": "2025-12-12T14:22:32.190172",
      "status": "queued",
      "execution_timestamp": null
    }
  ],
  "history": [
    {
      "job_id": 10,
      "submit_timestamp": "2025-12-12T14:22:32.190172",
      "status": "executed",
      "execution_timestamp": "2025-12-12T14:22:32.194734"
    }
  ]
}
```

## Data Structures Used

| Component | Data Structure | Purpose |
|-----------|---------------|---------|
| Job Queue | Linked List | FIFO ordering of pending jobs |
| History | Linked List | Sequential storage of executed jobs |
| Duplicate Check | Hash Table (Chaining) | O(1) average lookup for duplicates |

## Requirements

- Python 3.8+
- No external dependencies (uses only standard library)

## License

This project is created for educational purposes.
