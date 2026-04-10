"""
Code Executor Module

General purpose: This module provides a helper function for executing a Python
file as a subprocess for real-time I/O streaming.

Classes:
    TBD
Functions:
    code_executor(filepath): Creates a subprocess for the given Python file.
"""

import subprocess

"""
Function: code_executor(filepath)
Description: Creates a subprocess that executes the given Python file with
             unbuffered output and piped I/O streams.
@precondition:  The filepath must point to a valid, accessible Python file.
@postcondition: A subprocess.Popen instance is returned with stdin, stdout,
                and stderr piped and ready to stream.
@param filepath: The path to the Python file to execute.
@return: A subprocess.Popen instance representing the running process.
"""
def code_executor(filepath):
    return subprocess.Popen(["python", "-u", filepath],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=False,
                               bufsize=1)