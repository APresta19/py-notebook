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
        process = self.remove_process(self, sid)
        if process:
            process.terminate()
            process.wait()