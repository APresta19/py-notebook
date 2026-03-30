import socket from "./sockets/getSocketBackend.js";
import { getTerminal } from "./services/initTerminal.js";

export default function getSubmissionCode() {
    console.log("Clicked submission.");
    let compileButton = document.querySelector(".compile");
    

    // Determine button type
    if(!compileButton)
    {
        compileButton = document.querySelector(".stop-button");
    }

    // If the user presses the run button
    if(compileButton.textContent.includes("Run"))
    {
        // Get the code and add to local storage
        const code = window.monacoEditor.getValue();
        localStorage.setItem("code", code);

        // Clear terminal
        getTerminal()?.clearTerminal();

        // Change button to stop
        compileButton.textContent = "⏹ Stop";
        compileButton.classList.add("stop-button");
        compileButton.classList.remove("compile");

        // Emit the compile event with the code
        console.log("Code emitted: ", code);
        socket.emit("compile", { code: code });
    }
    else
    {
        // Stopping execution
        window.term.write("\n\x1b[1;31mProcess Stopped.\x1b[0m") // write in red
        socket.emit("stop_process");
    }
}

document.addEventListener("click", (e) => {
    if (e.target.classList.contains("compile") || e.target.classList.contains("stop-button")) 
    {
        getSubmissionCode();
    }
});