import unittest
import logging
from task_scheduler import Scheduler, HashTable, LinkedQueue, Job

# Configure logging for the test module
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def log_success(message: str):
    logging.info(f"SUCCESS: {message}")


class BaseLoggedTest(unittest.TestCase):
    """Base test case providing standardized START/END logging for all tests."""
    def setUp(self):
        test_name = self._testMethodName
        purpose = getattr(self, test_name).__doc__ or "Test case"
        logging.info(f"START: {test_name} - {purpose}")

    def tearDown(self):
        test_name = self._testMethodName
        logging.info(f"END: {test_name}\n")


class TestInsertion(BaseLoggedTest):
    def test_scheduler_submit_inserts_into_hash_and_queue(self):
        """Verify submitting a task inserts into both hash table and queue"""
        s = Scheduler(hash_size=5)
        job = s.submit_task(42)
        # Hash search should find it
        self.assertIsNotNone(s.hash.search(42))
        self.assertEqual(s.hash.search(42).job_id, 42)
        # Queue head should be the same job
        q_list = s.queue.to_list()
        self.assertEqual(len(q_list), 1)
        self.assertEqual(q_list[0].job_id, job.job_id)
        log_success("submit_task inserted Job(42) into hash and queue; queue head matches the inserted job")

    def test_duplicate_insertion_raises(self):
        """Ensure duplicate job IDs cannot be inserted into the scheduler"""
        s = Scheduler(hash_size=5)
        s.submit_task(7)
        with self.assertRaises(ValueError):
            s.submit_task(7)
        log_success("duplicate insertion raised ValueError as expected for Job(7)")


class TestSearching(BaseLoggedTest):
    def test_hash_table_search(self):
        """HashTable can find existing jobs and returns None for missing ones"""
        ht = HashTable(size=3)
        j1 = Job(10)
        j2 = Job(13)  # same bucket as 10 when size=3
        ht.insert(j1)
        ht.insert(j2)
        self.assertIs(ht.search(10), j1)
        self.assertIs(ht.search(13), j2)
        self.assertIsNone(ht.search(99))
        log_success("HashTable search retrieved Job(10) and Job(13); Job(99) returned None as expected")

    def test_scheduler_find_job_in_queue_and_history(self):
        """Scheduler.find_job locates job first in queue then in history after execution"""
        s = Scheduler(hash_size=3)
        s.submit_task(1)
        # Should be found in queue
        loc = s.find_job(1)
        self.assertIsNotNone(loc)
        self.assertEqual(loc[0], "queue")
        self.assertEqual(loc[1].job_id, 1)
        # Execute and then find in history
        s.run_next_task()
        loc2 = s.find_job(1)
        self.assertIsNotNone(loc2)
        self.assertEqual(loc2[0], "history")
        self.assertEqual(loc2[1].job_id, 1)
        log_success("Scheduler.find_job found Job(1) in queue before execution and in history after run_next_task()")


class TestDequeueing(BaseLoggedTest):
    def test_linked_queue_fifo(self):
        """LinkedQueue dequeues elements in FIFO order"""
        q = LinkedQueue()
        a, b, c = Job(1), Job(2), Job(3)
        q.enqueue(a)
        q.enqueue(b)
        q.enqueue(c)
        self.assertEqual(q.dequeue().job_id, 1)
        self.assertEqual(q.dequeue().job_id, 2)
        self.assertEqual(q.dequeue().job_id, 3)
        self.assertTrue(q.is_empty())
        log_success("LinkedQueue maintained FIFO order for Job IDs [1, 2, 3] and is empty after dequeueing all")

    def test_scheduler_run_next_task_updates_status_and_history(self):
        """Running next task sets status to executed, logs to history, and removes from hash/queue"""
        s = Scheduler(hash_size=5)
        s.submit_task(5)
        s.submit_task(6)
        executed = s.run_next_task()
        self.assertIsNotNone(executed)
        self.assertEqual(executed.status, "executed")
        self.assertEqual(len(s.history.display_history()), 1)
        # Ensure it was removed from the queue
        self.assertEqual([j.job_id for j in s.queue.to_list()], [6])
        # Since HashTable now stores history nodes, the job should still be retrievable
        self.assertIsNotNone(s.hash.search(5))
        self.assertEqual(s.hash.search(5).status, "executed")
        log_success("run_next_task executed Job(5), added to history, and the job remains retrievable from the hash as executed")


class TestCollisionHandling(BaseLoggedTest):
    def test_hash_table_chaining(self):
        """HashTable handles collisions via chaining; search and removal operate correctly"""
        # Small table to force collisions
        ht = HashTable(size=3)
        ids = [3, 6, 9]  # All collide into same bucket for size=3
        jobs = [Job(i) for i in ids]
        for j in jobs:
            ht.insert(j)
        # They should all be retrievable
        for i, j in zip(ids, jobs):
            self.assertIs(ht.search(i), j)
        # And removal should work FIFO in bucket order where matched
        removed = ht.remove(6)
        self.assertIsNotNone(removed)
        self.assertEqual(removed.job_id, 6)
        self.assertIsNone(ht.search(6))
        # Remaining still present
        self.assertIsNotNone(ht.search(3))
        self.assertIsNotNone(ht.search(9))
        log_success("HashTable chaining stored Jobs [3,6,9]; removal of Job(6) succeeded and others remained retrievable")


if __name__ == "__main__":
    unittest.main()
