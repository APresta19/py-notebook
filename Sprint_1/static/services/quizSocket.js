/**
 * Quiz Socket Module
 * General purpose: This module manages quiz generation and interaction by
 * communicating with the backend through socketio. It handles sending user code,
 * rendering quiz questions, collecting answers, and displaying results.
 * 
 * Classes:
 *     TBD
 * Functions:
 *     hideNextLessonButton
 *     showNextLessonButton
 *     generateQuestions
 *     submitAnswers
 */

const socket = io();
const quizPanel = document.querySelector('.quiz-panel');
const quizContent = document.getElementById('quiz-content');
const nextLessonButton = document.getElementById('next-lesson-button');

/**
 * Function: hideNextLessonButton()
 * Description: Hides and resets the "Next Lesson" button.
 * @precondition:  nextLessonButton must exist in the DOM.
 * @postcondition: The button is hidden and enabled.
 */
function hideNextLessonButton() {
    if (nextLessonButton) {
        nextLessonButton.hidden = true;
        nextLessonButton.disabled = false;
    }
}

/**
 * Function: showNextLessonButton()
 * Description: Displays the "Next Lesson" button if a valid next lesson id exists.
 * @precondition:  quizPanel and nextLessonButton must exist.
 * @postcondition: The button is shown if a next lesson id is present.
 */
function showNextLessonButton() {
    if (!quizPanel || !nextLessonButton) {
        return;
    }

    const nextLessonId = quizPanel.dataset.nextLessonId;
    if (!nextLessonId) {
        return;
    }

    nextLessonButton.hidden = false;
}

/**
 * Function: generateQuestions()
 * Description: Sends stored user code to the backend to generate quiz questions.
 *              Displays a loading message while waiting for a response.
 * @precondition:  Code must exist in localStorage under the key 'code'.
 * @postcondition: A 'submit_code' event is emitted or an error message is displayed.
 */
function generateQuestions() {
    const code = localStorage.getItem('code');

    if (!code) {
        hideNextLessonButton();
        quizContent.innerHTML =
            '<p style="color:red;">No code found - run your code first.</p>';
        return;
    }

    hideNextLessonButton();
    quizContent.innerHTML =
        '<p class="placeholder">Generating questions...</p>';

    socket.emit('submit_code', { code: code });
}

/**
 * Event: nextLessonButton click
 * Description: Navigates the user to the next lesson when the button is clicked.
 * @precondition:  nextLessonButton must exist and contain a valid nextLessonId.
 * @postcondition: The browser redirects to the next lesson URL.
 */
if (nextLessonButton) {
    nextLessonButton.addEventListener('click', () => {
        const nextLessonId = quizPanel?.dataset.nextLessonId;
        if (!nextLessonId) {
            return;
        }

        window.location.href = `/?lesson=${encodeURIComponent(nextLessonId)}`;
    });
}

/**
 * Event: window message
 * Description: Listens for a trigger of quiz generation.
 * @precondition:  event.data must contain type 'submit_code' and valid code.
 * @postcondition: Code is sent to backend and loading message is displayed.
 */
window.addEventListener('message', (event) => {
    if (event.data?.type === 'submit_code') {
        hideNextLessonButton();
        quizContent.innerHTML = '<p class="placeholder">Generating questions...</p>';
        socket.emit('submit_code', { code: event.data.code });
    }
});

/**
 * Socket Event: quiz_error
 * Description: Handles errors returned from the backend during quiz generation.
 * @precondition:  Socket connection must be active.
 * @postcondition: Error message is displayed and next lesson button is hidden.
 */
socket.on('quiz_error', (data) => {
    hideNextLessonButton();
    quizContent.innerHTML = `
        <p style="color:red;">Error: ${data.error}</p>
    `;
});

/**
 * Socket Event: quiz_ready
 * Description: Receives generated quiz questions and renders them in the UI.
 * @precondition:  data.questions must be a valid array of question objects.
 * @postcondition: Quiz questions are displayed with appropriate input fields.
 */
socket.on('quiz_ready', function(data) {
    hideNextLessonButton();
    quizContent.innerHTML = '<h3>Answer the Questions:</h3>';

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
        quizContent.innerHTML += html;
    });

    quizContent.innerHTML += `
        <br>
        <button onclick="submitAnswers()">Submit Answers</button>
    `;
});

/**
 * Function: submitAnswers()
 * Description: Collects all user inputs from the quiz and sends them to the backend.
 * @precondition:  Quiz inputs must exist within #quiz-content.
 * @postcondition: A 'submit_answers' event is emitted with the collected answers.
 */
function submitAnswers() {
    const inputs = document.querySelectorAll('#quiz-content input');
    let answers = {};

    inputs.forEach(input => {
        if (input.type === 'radio') {
            if (input.checked) {
                answers[input.name] = input.value;
            }
        } else {
            answers[input.name] = input.value;
        }
    });

    socket.emit('submit_answers', { answers: answers });
}

/**
 * Socket Event: quiz_results
 * Description: Receives quiz results, displays feedback, and updates completion state.
 * @precondition:  data.results must contain evaluated answers.
 * @postcondition: Results are displayed, score is shown, and completion event is emitted.
 */
socket.on('quiz_results', function(data) {
    let correctCount = 0;
    let html = '<h3>Results:</h3>';

    data.results.forEach(r => {
        const color = r.is_correct ? '#4CAF50' : '#ff4d4d';

        if (r.is_correct) correctCount++;

        html += `
            <div class="question-block">
                <p><strong>${r.question}</strong></p>
                <p>Your Answer: ${r.user_answer}</p>
                <p style="color:${color}">
                    ${r.is_correct ? 'Correct!' : 'Incorrect (Correct: ' + r.correct_answer + ')'}
                </p>
            </div>
        `;
    });

    window.testComplete = true;
    socket.emit('quiz_completed', { score: correctCount, total: data.results.length });

    html += `<h3>Score: ${correctCount} / ${data.results.length}</h3>`;

    quizContent.innerHTML = html;
    showNextLessonButton();
});
