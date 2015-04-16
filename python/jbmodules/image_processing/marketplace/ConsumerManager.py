#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import multiprocessing
from Queue import Empty

class Consumer(multiprocessing.Process):

    def __init__(self, todo_queue, task_queue, consumers_finished):
        multiprocessing.Process.__init__(self)
        self.todo_queue = todo_queue
        self.task_queue = task_queue
        self.consumers_finished = consumers_finished

    def run(self):
        while not all(flag for flag in self.consumers_finished.values()):
            try:
                task = self.todo_queue.get(False)
                self.consumers_finished[self.name] = False
            except Empty:
                self.task_queue.put("STOP")
                self.consumers_finished[self.name] = True
            else:
                task_result = self.process_data(task)
                self.task_queue.put(task_result)

    def process_data(self, html):
        print "Processing %s" % html
        return html