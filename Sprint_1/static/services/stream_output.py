"""
Stream Output Module
General purpose: This module provides functions for streaming output and errors 
from a running process back to the client through WebSockets.
It reads process output in chunks and emits them as socketio events in real time.

Classes:
    TBD
Functions:
    stream_output(p, sid):        Streams stdout from the running process to the client,
                                  then delegates to stream_error_output when stdout is empty.
    stream_error_output(p, sid):  Streams stderr from the running process to the client.
"""

from static.sockets.getSocketIO import socketio


"""
Function: stream_output(p, sid=None)
Description: Reads output from the given process in chunks and emits each chunk
             to the client as an 'output' Socket.IO event. When it runs out of output,
             stream_error_output is called to handle any error output.
@precondition:  The process p must be active with a readable stdout stream.
                The socketio instance must be initialized.
@postcondition: All available output is emitted to the client. If the output stream is empty,
                stderr is then checked and streamed thorugh stream_error_output.
@param p:   The running process whose output will be streamed.
@param sid: The socketio session id of the client.
"""
def stream_output(p, sid = None):
    print("Streaming output for ", p)
    while True:
        char = p.stdout.read1(1024) # Read output in chunks of 1024 bytes
        
        # If no more output, check for errors
        if not char:
            stream_error_output(p, sid)
            break

        # Emit output to client
        socketio.emit("output", char.decode("utf-8"), to=sid)
        if p.poll() is not None:
            break

"""
Function: stream_error_output(p, sid=None)
Description: Reads error output from the given process in chunks and emits each chunk
             to the client as an 'error-output' socketio event.
@precondition:  The process p must have a readable error stream.
                The socketio instance must be initialized.
@postcondition: All available error output is emitted to the client as 'error-output' events.
@param p:   The running process whose error output will be streamed.
@param sid: The socketio session id of the client.
"""
def stream_error_output(p, sid = None):
    while True:
        char = p.stderr.read1(1024) # Read error output in chunks of 1024 bytes

        # If no more error output, break the loop
        if not char:
            break

        # Emit error output to client
        socketio.emit("error-output", char.decode("utf-8"), to=sid)
        if p.poll() is not None:
            break