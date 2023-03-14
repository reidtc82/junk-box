# Junkbox driver that manages the execution of jobs
# executors form a distributed mesh network
# the driver will send jobs to the executors
# the executors will execute the jobs
# the executors will return the results to the driver
# the driver will manage the execution of jobs

# The driver communicates with the executors using a socket connection
# the driver maintains a job queue and a result queue
# It will monitor the heartbeat of the executor and if it fails it will remove it from the mesh network
# If the driver removes a node from the mesh network it will reassign the jobs that were assigned to that node
# that means teh executor needs to be able to handle the reassignment of jobs
# and that it can track which jobs are assigned to which executors

# The driver is passed to the Math class
# The Math class will use the driver to execute jobs
# The Math class will return the results to the user

# The math class will give the driver a list of cells to be executed
# those cell smay be a single cell or a JunkBox object
# the math class wil also pass the function to perform on each

# executors will connect to the driver through a socket and add themselves to the executor list in doing so

import asyncio
import itertools
import uuid
from multiprocessing import Process


class State:
    STOPPED = 1
    RUNNING = 2
    PAUSED = 3


class JunkBoxPool:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.tasks = {}

    def __enter__(self, *args, **kwargs):
        return self

    # __exit__ for this class when used as a context manager
    def __exit__(self, *args, **kwargs):
        pass

    def apply_async(self, target, args) -> str:
        coro = target(*args)
        self.tasks[str(uuid.uuid4())] = self.loop.create_task(coro)

    def join(self):
        yield from asyncio.gather(*self.tasks.values())
