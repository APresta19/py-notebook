"""
Function: write_input(process, output_data)
Description: Writes the given input data to the stdin of the given subprocess
             and flushes the buffer to ensure immediate delivery.
@precondition:  The process must be active with an open, writable stdin stream.
                output_data must be bytes-encoded.
@postcondition: The data is written to the process stdin and the buffer is flushed.
@param process:     The active subprocess.Popen instance to write input to.
@param output_data: The bytes-encoded input data to write to stdin.
"""

def write_input(process, output_data):
    # Write to stdin and flush
    process.stdin.write(output_data)
    process.stdin.flush()