import socketio

def stream_output(p, sid = None):
    while True:
        char = p.stdout.read1(1024)
        if not char:
            stream_error_output(p, sid)
            break
        socketio.emit("output", char.decode("utf-8"), to=sid)
        if p.poll() is not None:
            break

def stream_error_output(p, sid = None):
    while True:
        char = p.stderr.read1(1024)
        if not char:
            break
        socketio.emit("error-output", char.decode("utf-8"), to=sid)
        if p.poll() is not None:
            break