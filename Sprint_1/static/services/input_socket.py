from flask import request
from static.services.write_input import write_input
from static.services.stream_output import stream_output

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