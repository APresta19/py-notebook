// static/services/quizSocket.js

const socket = io();

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

/*
socket.on('quiz_ready', (data) => {
    const panel = document.querySelector('.quiz-panel');
    panel.innerHTML = '<h2>Quiz</h2>';
    data.questions.forEach(q => {
        const p = document.createElement('p');
        p.textContent = q.question;
        panel.appendChild(p);
    });
});
*/

socket.on('quiz_error', (data) => {
    document.querySelector('.quiz-panel').innerHTML = `
        <h2>Quiz</h2>
        <p style="color:red;">Error: ${data.error}</p>
    `;
});

socket.on('quiz_ready', function(data) {
    const container = document.getElementById("quiz-content");

    container.innerHTML = "<h3>Answer the Questions:</h3>";

    data.questions.forEach(q => {
        let html = `<div class="question-block">`;
        html += `<p>${q.question}</p>`;

        if (q.options) {
            q.options.forEach(opt => {
                html += `
                    <label>
                        <input type="radio" name="${q.id}" value="${opt}">
                        ${opt}
                    </label><br>
                `;
            });
        } else {
            html += `<input type="text" name="${q.id}"><br>`;
        }

        html += `</div>`;
        container.innerHTML += html;
    });

    container.innerHTML += `
        <br>
        <button onclick="submitAnswers()">Submit Answers</button>
    `;
});

function submitAnswers() {
    const inputs = document.querySelectorAll("#quiz-content input");
    let answers = {};

    inputs.forEach(input => {
        if (input.type === "radio") {
            if (input.checked) {
                answers[input.name] = input.value;
            }
        } else {
            answers[input.name] = input.value;
        }
    });

    socket.emit("submit_answers", {
        answers: answers
    });
}

socket.on("quiz_results", function(data) {
    const container = document.getElementById("quiz-content");

    container.innerHTML = "<h3>Results:</h3>";

    let correctCount = 0;
    let html = "<h3>Results:</h3>";

    data.results.forEach(r => {
        const color = r.is_correct ? "#4CAF50" : "#ff4d4d";
        
        if (r.is_correct) correctCount++;

        html += `
            <div class="question-block">
                <p><strong>${r.question}</strong></p>
                <p>Your Answer: ${r.user_answer}</p>
                <p style="color:${color}">
                    ${r.is_correct ? "Correct!" : "Incorrect (Correct: " + r.correct_answer + ")"}
                </p>
            </div>
        `;
    });
    //Window test complete variable for Andrew's piece

    window.testComplete = true;
    //
    socket.emit("quiz_completed", { score: correctCount, total: data.results.length });
    
    html += `<h3>Score: ${correctCount} / ${data.results.length}</h3>`;

    container.innerHTML = html;
});