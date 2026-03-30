from static.sockets.getSocketIO import socketio
from static.services.code_executor import code_executor
from static.services.stream_output import stream_output
import threading
from static.services.process_manager import ProcessManager
from flask import request

process = None
process_manager = ProcessManager()

def register_compile_socket(socketio, process_manager):
    print("Registering compile socket")
    @socketio.on('compile')
    def compile_button(data):
        # Emit compile process event to client
        socketio.emit("compile_process")

        # File, code, submission id creation
        fp = "submissions/submission.py"
        code = data["code"]
        sid = request.sid

        # Open new file and write code to it
        with open(fp, "w", newline="\n") as f:
            f.write(code)

        process = code_executor(fp)

        process_manager.add_process(sid, process)

        stream_output(process, sid)

        thread = threading.Thread(target=stream_output, daemon=True)
        thread.start()

        # Program has stopped
        stop_compile_process(process)

    def stop_compile_process(process):
        socketio.emit("process_done")
        process.wait()