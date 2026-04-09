/*
Get Socket Backend Module
General purpose: This module initializes and exports the shared socket instance
used across the application for JavaScript files.
*/

const socket = io("http://localhost:5000");
export default socket;