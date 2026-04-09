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

export function getTerminal()
{
    return terminalInstance;
}