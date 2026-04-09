"""
Compile Socket Module

General purpose: This module registers the socketio event handler for compilation requests. 
It listens for compile events, writes the submitted code to a file, executes it, 
streams the output back to the client, and emits a completion event when the process finishes.

Module level attributes:
    process (None):                   Tracks the current process running.
    process_manager (ProcessManager): Manages active processes.
Classes:
    TBD
Functions:
    register_compile_socket(socketio, process_manager): Registers the 'compile'
                                                        socketio event handler for
                                                        processing compilation requests.
"""

from static.sockets.getSocketIO import socketio
from static.services.code_executor import code_executor
from static.services.stream_output import stream_output
import threading
from static.services.process_manager import ProcessManager
from flask import request

process = None
process_manager = ProcessManager()

"""
Function: register_compile_socket(socketio, process_manager)
Description: Registers the 'compile' socketio event handler, which listens for
             compilation requests, writes submitted code to a file, executes it,
             streams output to the client, and emits a completion event when done.
@precondition:  The socketio instance must be initialized and a ProcessManager
                instance must be available with an active process for the given sid.
@postcondition: The 'compile' socketio event handler is registered. For each
                'compile' event, the code is written to file, executed, streamed,
                and a 'process_done' event is emitted to the client on completion.
@param socketio:         The socketio server instance used to register event handlers.
@param process_manager:  The shared ProcessManager instance for storing active processes.
"""
def register_compile_socket(socketio, process_manager):
    print("Registering compile socket")
    @socketio.on('compile')
    def compile_button(data):
        print("Emitting compile process")
        # Emit compile process event to client
        socketio.emit("compile_process") # Lets the client know we have compiled

        # File, code, submission id creation
        fp = "submissions/submission.py"
        code = data["code"]
        sid = request.sid

        # Open new file and write code to it
        with open(fp, "w", newline="\n") as f:
            f.write(code)

        # Execute code and store current process
        process = code_executor(fp)

        # Add the process to the process manager
        process_manager.add_process(sid, process)

        # Stream output
        stream_output(process, sid)

        # Start a thread to allow for concurrent I/O
        thread = threading.Thread(target=stream_output, args=(process, sid), daemon=True)
        thread.start()

        # Program has stopped
        stop_compile_process(process)

    # Helper to emit 'process_done'
    def stop_compile_process(process):
        socketio.emit("process_done")
        process.wait()