window.getSubmissionCode = function() {
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

        // Clear previous output
        document.querySelector(".output").textContent = "";
        document.querySelector(".error-output").textContent = "";

        // Clear terminal
        window.clearTerminal();

        // Change button to stop
        compileButton.textContent = "⏹ Stop";
        compileButton.classList.add("stop-button");
        compileButton.classList.remove("compile");

        const problemStr = document.querySelector(".problem-text").textContent;
        const num = Number(problemStr.substring(problemStr.indexOf(" ")+1, problemStr.length));

        // Emit the compile event with the code
        socket.emit("compile", {code: code });
    }
    else
    {
        // Stopping execution
        window.term.write("\n\x1b[1;31mProcess Stopped.\x1b[0m") // write in red
        socket.emit("stop_process");
    }
}