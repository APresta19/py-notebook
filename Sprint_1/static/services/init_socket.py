from flask import Flask, render_template, request
from flask_socketio import emit
from localStoragePy import localStoragePy
from static.services.process_manager import ProcessManager
from static.sockets.getSocketIO import socketio
from controller import process_code

process_manager = ProcessManager()

compile_files = []

def init_socket():

    @socketio.on('submit_code')
    def handle_code_submission(data):
        print(">>> submit_code received")          # confirm event arrived
        code = data.get('code', '')
        print(f">>> code length: {len(code)}")

        if not code.strip():
            emit('quiz_error', {'error': 'No code received'})
            return

        response = process_code(code)
        print(f">>> process_code response: {response}")  # confirm questions generated

        if not response["success"]:
            emit('quiz_error', {'error': response['error']})
        else:
            print(f">>> emitting quiz_ready with {len(response['questions'])} questions")
            emit('quiz_ready', {'questions': response['questions']})
            
    @socketio.on("connect")
    def handle_connect():
        #create_files(10)
        print("Client has been connected")

    @socketio.on("stop_process")
    def stop_process():
        sid = request.sid
        process_manager.terminate_process(sid)
        print("Process stopped for socket id: ", sid)
        

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








'''@app.route("/team-facing")
def index():
    return render_template('render.html')


def create_files(max_files):
    global compile_files
    for i in range(max_files):
        fp = "submissions/submission" + str(i+1) + ".py"
        with open(fp, "w") as f:
            print("File ", i+1, "created")
            compile_files.append(fp)
    print("Compiled Files: ", compile_files)

@socketio.on('process_done')
def process_done():
    process.stdin.flush()

#if __name__ == "__main__":
    #socketio.run(app, debug=True)'''