export class TerminalManager
{
    constructor(socket, component)
    {
        this.socket = socket;
        this.term = new Terminal({
            theme: {
                background: '#1e1e1e',
                scrollbar: '#4e4e4e'
            },
            cursorBlink: true,
        });
        this.inputStr = "";
        this.hasCompiled;

        window.term = this.term;
        this.term.open(component);

        this.setupTerminal();
        this.setupTerminalSockets();
    }

    setupTerminal()
    {
        this.term.onData((data) => {
            if(!this.hasCompiled) return;
            this.handleInputTerminal(data);
        });
        
    }

    setupTerminalSockets() {
        console.log("Setting up terminal sockets.");

        this.socket.on("output", (line) => {
            console.log("Output line: ", line);
            this.term.write(line);
        });

        this.socket.on("error-output", (line) => {
            this.term.write("\x1b[31m" + line + "\x1b[0m");
        });

        this.socket.on("compile_process", () => {
            this.hasCompiled = true;
        });

        this.socket.on("process_done", () => {
            this.hasCompiled = false;
            this.updateCompileButton();
        });
    }

    handleInputTerminal(data)
    {
        // Check for enter press
        // If not enter --> write to terminal
            // If backspace --> remove
            // If not enter and not backspace --> append to array/string
        // If enter
            // Stuff at bottom (input_added)
            // Send string
            // Clear string
        if (data != "\r") // Enter
        {
            if (data == "\x7f") // Backspace
            {
                if (this.inputStr.length > 0)
                {
                    this.term.write("\b \b"); // Backspace escape sequence
                    this.inputStr = this.inputStr.substring(0, this.inputStr.length-1) // Remove last char
                }
            }
            else {
                this.term.write(data);
                this.inputStr += data;
            }
        }
        else // Pressed enter
        {
            this.socket.emit("input_added", this.inputStr);
            this.inputStr = "";
            this.term.write("\r\n"); // Newline
        }
    }

    clearTerminal()
    {
        this.inputStr = "";
        this.term.reset();
    }

    updateCompileButton() {
        const btn = document.querySelector(".stop-button");
        if (!btn) return;

        btn.textContent = "▶ Run";
        btn.classList.add("compile");
        btn.classList.remove("stop-button");
    }

}