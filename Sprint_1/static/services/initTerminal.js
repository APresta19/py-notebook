/**
 * Init Terminal Module
 * 
 * General purpose: This module initializes the terminal instance upon a successful
 * WebSocket connection and can be used as a getter for the terminal across the project.
 * 
 * Module level attribute:
 *     terminalInstance (TerminalManager | null): The active terminal instance. Null until
 *                                                a socket connection is established.
 * Classes:
 *     TBD
 * Functions:
 *     getTerminal(): Returns the active TerminalManager instance.
 */

import { TerminalManager } from "./terminalManager.js";
import socket from "../sockets/getSocketBackend.js";

let terminalInstance = null;
console.log("initTerminal.js loaded");
socket.on("connect", () => {
    console.log("Client connected successfully.");
    console.log("Socket ID:", socket?.id);
    const terminalComponent = document.getElementById("terminal");
    terminalInstance = new TerminalManager(socket, terminalComponent);
})

/**
 * Function: getTerminal()
 * Description: Returns the active TerminalManager instance
 * @precondition:  A socket connection must have been established and the TerminalManager
 *                 must have been instantiated via the 'connect' event handler.
 * @postcondition: The current terminalInstance is returned. May be null if it's called before
 *                 the socket connection creation.
 * @return {TerminalManager | null} The active TerminalManager instance, or null if not yet initialized.
 */
export function getTerminal()
{
    return terminalInstance;
}