import socketio
import code_executor
import stream_output
import threading
from process_manager import ProcessManager

process = None
process_manager = ProcessManager()

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
    stop_compile_process()

def stop_compile_process():
    socketio.emit("process_done")
    process.wait()