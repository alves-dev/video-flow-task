import queue
import threading

from app.domain.types import Task


class TaskQueue:

    def __init__(self):
        self.queue = queue.Queue()
        self.current_task = None

        self.tasks_in_queue = set()
        self.lock = threading.Lock()

        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()

    def add_task(self, task: Task):
        with self.lock:
            if task.name in self.tasks_in_queue:
                return False

            self.tasks_in_queue.add(task.name)
            self.queue.put(task)
            return True

    def _worker_loop(self):
        while True:
            task = self.queue.get()

            try:
                self.current_task = task.name
                task.func(*task.args)
            except Exception as e:
                print("Erro na task:", e)
            finally:
                with self.lock:
                    self.tasks_in_queue.discard(task.name)
                self.current_task = None
                self.queue.task_done()

    def status(self):
        return {
            "current_task": self.current_task,
            "queue_size": self.queue.qsize()
        }


task_queue = TaskQueue()
