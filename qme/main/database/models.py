"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.logger import bot
import json
import sys


try:
    from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, func
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, backref
    from uuid import uuid4
except:
    sys.exit("sqlalchemy is required for a non-filesystem database.")

# Shared declarative base
Base = declarative_base()


class Task(Base):
    """An executor task. The id is prefixed with the executor type, and must
       be unique.
    """

    __tablename__ = "task"
    taskid = Column(String(150), primary_key=True)
    command = Column(String(500))
    timestamp = Column(DateTime, default=func.now())
    executor_name = Column(String(50))
    data = relationship("TaskData", uselist=False, back_populates="task")  # one-to-one

    def __init__(self, taskid=None, executor=None, command=None):
        self.taskid = taskid
        self.executor_name = executor
        self.command = command

    def summary(self):
        return self.executor.summary()

    def load(self):
        """loading a task means exporting as json"""
        data = {
            "executor": self.executor_name,
            "uid": self.taskid,
            "data": {},
            "command": self.command,
        }

        if self.data and self.data.data:
            data["data"] = json.loads(self.data.data)

        return data

    def export(self):
        """Export removes the outer wrapper, and just returns the data"""
        return self.load().get("data", {})

    def __repr__(self):
        return "<Task %r>" % self.taskid


class TaskData(Base):
    """a task data object includes custom data for an executor (json)"""

    __tablename__ = "taskdata"
    id = Column(Integer, primary_key=True)
    taskid = Column(String, ForeignKey("task.taskid"))
    timestamp = Column(DateTime, default=func.now())
    data = Column(Text, nullable=True)
    task = relationship("Task", back_populates="data")

    def __repr__(self):
        return "<TaskData %r>" % self.taskid