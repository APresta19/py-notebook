"""
Process Manager Module

General purpose: This module provides the ProcessManager class for managing active
subprocess instances. It allow for adding, retrieving,
removing, and terminating processes.

Classes:
    ProcessManager: Manages a dictionary of active subprocesses with a key of socket session ID.
Functions:
    TBD
"""

"""
Class: ProcessManager
Description: Manages active subprocess instances associated with socketio session ids.
             Provides methods to add, retrieve, remove, and terminate processes.
@precondition:  A valid socketio session id must be provided.
@postcondition: Processes are stored, retrieved, or cleaned up.
"""
class ProcessManager:
    def __init__(self):
        self.processes = {}

    def add_process(self, sid, process):
        self.processes[sid] = process

    def remove_process(self, sid):
        return self.processes.pop(sid, None)
    
    def get_process(self, sid):
        return self.processes.get(sid)
    
    def terminate_process(self, sid):
        process = self.remove_process(sid)
        if process:
            process.terminate()
            process.wait()