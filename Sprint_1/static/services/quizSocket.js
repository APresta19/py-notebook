// static/services/quizSocket.js

const socket = io('http://127.0.0.1:5000');

function generateQuestions() {
    const code = localStorage.getItem('code');

    if (!code) {
        document.getElementById('quiz-content').innerHTML = 
            '<p style="color:red;">No code found — run your code first.</p>';
        return;
    }

    document.getElementById('quiz-content').innerHTML = 
        '<p class="placeholder">Generating questions...</p>';
    
    socket.emit('submit_code', { code: code });
}

window.addEventListener('message', (event) => {
    if (event.data?.type === 'submit_code') {
        document.querySelector('.quiz-panel').innerHTML = `
            <h2>Quiz</h2>
            <p class="placeholder">Generating questions...</p>
        `;
        socket.emit('submit_code', { code: event.data.code });
    }
});

socket.on('quiz_ready', (data) => {
    const panel = document.querySelector('.quiz-panel');
    panel.innerHTML = '<h2>Quiz</h2>';
    data.questions.forEach(q => {
        const p = document.createElement('p');
        p.textContent = q.question;
        panel.appendChild(p);
    });
});

socket.on('quiz_error', (data) => {
    document.querySelector('.quiz-panel').innerHTML = `
        <h2>Quiz</h2>
        <p style="color:red;">Error: ${data.error}</p>
    `;
});