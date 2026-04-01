import { TerminalManager } from "../services/terminalManager";

// Socket
const socket = io("http://localhost:5000");

const terminalComponent = document.getElementById("terminal"); 
new TerminalManager(socket, terminalComponent);