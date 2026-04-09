"""
Initialize Socket Module

General purpose: This module serves to initialize and register all 
socket event handlers for the application. It handles client connections, disconnections, 
process termination, compilation requests, and input handling through WebSockets.

Classes:
    TBD
Functions:
    init_socket():  Registers all socketio event handlers for client connection,
                    disconnection, process termination, compilation, and input handling.
"""

from flask import request
from static.services.process_manager import ProcessManager
from static.sockets.getSocketIO import socketio

process_manager = ProcessManager()

"""
Function: init_socket()

Description: This function registers all Socket.IO event handlers for client connection,
             disconnection, process termination, compilation, and input handling.

@precondition: The socketio instance must be initialized and the ProcessManager must be available 
               for managing processes.
@postcondition: All relevant socketio event handlers will be registered, 
                allowing the application to handle necessary events through WebSockets.
"""
def init_socket():
    # Client connection handler
    @socketio.on("connect")
    def handle_connect():
        print("Client has been connected")

    # Process termination handler
    @socketio.on("stop_process")
    def stop_process():
        sid = request.sid
        process_manager.terminate_process(sid)
        print("Process stopped for socket id: ", sid)
        
    # Client disconnection handler
    @socketio.on("disconnect")
    def handle_disconnect():
        socket_id = request.sid
        process_manager.terminate_process(socket_id)
        print("Client disconnected")

    # Handle compile and input sockets
    from static.services.compile_socket import register_compile_socket
    from static.services.input_socket import register_input_socket

    register_compile_socket(socketio, process_manager)
    register_input_socket(socketio, process_manager)