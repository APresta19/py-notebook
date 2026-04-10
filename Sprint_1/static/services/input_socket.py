"""
Input Socket Module

General purpose: This module registers the socketio event handler for handling
user input sent through WebSockets. It listens for input events, writes the input
to the active process, and streams the resulting output back to the client.

Classes:
    TBD
Functions:
    register_input_socket(socketio, process_manager): Registers the 'input_added' 
                                                      Socket.IO event handler for 
                                                      processing user input.
"""

from flask import request
from static.services.write_input import write_input
from static.services.stream_output import stream_output

"""
Function: register_input_socket(socketio, process_manager)
Description: Registers the 'input_added' socketio event handler, which listens for
             user input, writes it to the running process, and streams output back.
@precondition:  The socketio instance must be initialized and a ProcessManager
                instance must be available with an active process for the given sid.
@postcondition: The 'input_added' socketio event handler is registered and the
                application is ready to handle user input and subsequently stream output through WebSockets.
@param socketio:         The socketio server instance used to register event handlers.
@param process_manager:  The shared ProcessManager instance for storing active processes.
"""
def register_input_socket(socketio, process_manager):
    @socketio.on('input_added')
    def input_added(data):
        # Get socket id
        sid = request.sid

        # Set I/O data
        process = process_manager.get_process(sid)
        output_data = (data + "\n").encode("utf-8")

        # Write input and stream output
        write_input(process, output_data)
        stream_output(process, sid)