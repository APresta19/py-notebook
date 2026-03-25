import subprocess

def code_executor(filepath):
    return subprocess.Popen(["python", "-u", filepath],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=False,
                               bufsize=1)