def write_input(process, output_data):
    process.stdin.write(output_data)
    process.stdin.flush()