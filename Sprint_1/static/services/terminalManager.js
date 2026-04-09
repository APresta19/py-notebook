/**
 * Terminal Manager Module
 * General purpose: This module defines the TerminalManager class, which manages
 * the xterm.js terminal instance, handles user input, and communicates with the
 * backend through WebSocket events for streaming output, error output, and input handling.
 * 
 * Classes:
 *     TerminalManager: Manages the terminal UI, input handling, and socket communication.
 * Functions:
 *     TBD
 */

/**
 * Class: TerminalManager
 * Description: Manages the xterm.js terminal instance and
 *              a socketio connection. Handles terminal setup, user input processing,
 *              and real-time output streaming from the backend.
 * @precondition:  A valid socketio instance and a terminal DOM element must be provided.
 * @postcondition: The terminal is rendered, event handlers are registered, and the
 *                 instance is ready to handle compilation and input events.
 */
export class TerminalManager
{
    /**
     * Function: constructor(socket, component)
     * Description: Initializes the TerminalManager by creating the xterm.js terminal,
     *              opening it on the provided DOM component, and setting up input
     *              and socket event handlers.
     * @precondition:  socket must be an active socketio instance. The component must be
     *                 a valid DOM element.
     * @postcondition: The terminal is rendered and all event handlers are registered.
     * @param {SocketIO} socket:       The active socketio client instance.
     * @param {HTMLElement} component: The DOM element to put the terminal on.
     */
    constructor(socket, component)
    {
        // Initialize socket, terminal, inputStr, and hasCompiled
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

        // Attach terminal to the window
        window.term = this.term;
        this.term.open(component);

        // Setup terminal and sockets
        this.setupTerminal();
        this.setupTerminalSockets();
    }

    /**
     * Function: setupTerminal()
     * Description: Registers the xterm.js onData handler to capture user key events
     *              and route them to handleInputTerminal when a process is running.
     * @precondition:  The terminal instance must be initialized and opened.
     * @postcondition: The onData handler is registered. Input is ignored until hasCompiled is true.
     */
    setupTerminal()
    {
        this.term.onData((data) => {
            if(!this.hasCompiled) return;
            this.handleInputTerminal(data);
        });
        
    }

     /**
     * Function: setupTerminalSockets()
     * Description: Registers all socketio event listeners for streaming stdout, stderr,
     *              compile start, and process completion events to the terminal.
     * @precondition:  The socket instance must be active and the terminal must be initialized.
     * @postcondition: Socket listeners for 'output', 'error-output', 'compile_process',
     *                 and 'process_done' are registered and ready to handle events.
     */
    setupTerminalSockets() {
        console.log("Setting up terminal sockets.");

        this.socket.on("output", (line) => {
            console.log("Output line: ", line);
            this.term.write(line);
        });

        this.socket.on("error-output", (line) => {
            this.term.write("\x1b[31m" + line + "\x1b[0m"); // Write the error line in red
        });

        this.socket.on("compile_process", () => {
            this.hasCompiled = true;
        });

        this.socket.on("process_done", () => {
            this.hasCompiled = false;
            this.updateCompileButton();
        });
    }

    /**
     * Function: writeToTerminal(msg)
     * Description: Writes a message directly to the terminal display.
     * @precondition:  The terminal instance must be initialized and opened.
     * @postcondition: The message is written and visible in the terminal.
     * @param {string} msg: The message to write to the terminal.
     */
    writeToTerminal(msg) {
        this.term.write(msg);
    }

    /**
     * Function: handleInputTerminal(data)
     * Description: Processes a key event captured from the terminal. Handles backspace,
     *              regular character input, and enter key to emit input to the backend.
     * @precondition:  hasCompiled must be true. data must be a valid key event string.
     * @postcondition: The key event shows in the terminal and inputStr is updated.
     *                 On enter, 'input_added' is emitted to the backend and inputStr is cleared.
     * @param {string} data: The keystroke data captured from xterm.js onData.
     */
    handleInputTerminal(data)
    {
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

    /**
     * Function: clearTerminal()
     * Description: Clears the terminal display.
     * @precondition:  The terminal instance must be initialized.
     * @postcondition: The terminal is visually reset and inputStr is cleared.
     */
    clearTerminal()
    {
        this.inputStr = "";
        this.term.reset();
    }

    /**
     * Function: updateCompileButton()
     * Description: Updates the compile/stop button in the UI back to its default
     *              state after a process finishes.
     * @precondition:  A DOM element with the class 'stop-button' must exist.
     * @postcondition: The button text is set to '▶ Run', the 'compile' class is added,
     *                 and the 'stop-button' class is removed.
     */
    updateCompileButton() {
        const btn = document.querySelector(".stop-button");
        if (!btn) return;

        btn.textContent = "▶ Run";
        btn.classList.add("compile");
        btn.classList.remove("stop-button");
    }

}