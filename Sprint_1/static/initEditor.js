/**
 * Init Editor Module
 * 
 * General purpose: This module provides utility functions for initializing the
 * Monaco editor with previously saved code from localStorage. It sets the editor
 * value once the Monaco instance is ready, retrying if necessary.
 *
 * Classes:
 *     TBD
 * Functions:
 *     initEditor():          Checks localStorage for saved code and initializes the editor.
 *     setEditorValue(code):  Sets the Monaco editor value, retrying until the instance is ready.
 */

/**
 * Function: initEditor()
 * Description: Checks localStorage for previously saved code and calls setEditorValue
 *              to populate the Monaco editor if valid code is found.
 * @precondition:  localStorage must be accessible in the current browser context.
 * @postcondition: If saved code exists, the editor is populated via setEditorValue.
 *                 No action is taken if localStorage is empty or null.
 */
export function initEditor()
{
    if(localStorage.getItem("code") != null && localStorage.getItem("code") != "")
    {
        const code = localStorage.getItem("code");
        console.log("Code: ", code);
        setEditorValue(code);
    }
}

/**
 * Function: setEditorValue(code)
 * Description: Sets the value of the Monaco editor to the provided code string.
 *              If the Monaco instance is not yet ready, retries every 100ms until it is.
 * @precondition:  code must be a non-null string. window.monacoEditor will be available
 *                 once the Monaco editor has finished loading.
 * @postcondition: The editor model value is set to the provided code. Retries are
 *                 cleared once the editor is successfully found and updated.
 * @param {string} code: The code string to set as the editor content.
 */
function setEditorValue(code) {
    if (window.monacoEditor) {
        console.log("Found editor");
        window.monacoEditor.getModel().setValue(code); // Set the Monaco editor value
    } else {
        console.log("Did not find editor. Waiting...");
        // editor not ready yet, retry after a short delay
        setTimeout(() => setEditorValue(code), 100);
    }
}