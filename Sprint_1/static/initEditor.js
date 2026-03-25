
// Initializes the editor based on previous code
export function initEditor()
{
    if(localStorage.getItem("code") != null && localStorage.getItem("code") != "")
    {
        const code = localStorage.getItem("code");
        console.log("Code: ", code);
        setEditorValue(code);
    }
}

// Sets the starter text for the editor
function setEditorValue(code) {
    if (window.monacoEditor) {
        console.log("Found editor");
        window.monacoEditor.getModel().setValue(code);
    } else {
        console.log("Did not find editor. Waiting...");
        // editor not ready yet, retry after a short delay
        setTimeout(() => setEditorValue(code), 100);
    }
}