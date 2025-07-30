// frontend/src/app.js
import { getQuestions, registerUser, loginUser, submitAnswer, getUserProfile } from './js/services/api.js';

// Import your components (assuming they are plain JS functions or classes)
// import { renderQuizQuestion } from './js/components/QuizQuestion.js';
// import { renderScoreDisplay } from './js/components/ScoreDisplay.js';

document.addEventListener('DOMContentLoaded', async () => {
    console.log("Frontend App Loaded!");

    const questionsContainer = document.createElement('div');
    questionsContainer.id = 'questions-container';
    document.body.appendChild(questionsContainer); // Append to body or a specific div

    // Example of fetching and displaying questions
    try {
        const questions = await getQuestions();
        console.log("Fetched questions:", questions);

        questionsContainer.innerHTML = '<h2>Quiz Questions:</h2>';
        questions.forEach(q => {
            const questionElement = document.createElement('div');
            questionElement.className = 'question-item';
            questionElement.innerHTML = `
                <h3>${q.text}</h3>
                <p>Options: ${q.options.join(', ')}</p>
                <p>Correct: ${q.correct_answer}</p>
                <button onclick="handleAnswer('${q._id}', '${q.options[0]}')">Answer with first option</button>
                <hr>
            `;
            questionsContainer.appendChild(questionElement);
        });

    } catch (error) {
        console.error("Failed to load questions in app.js:", error);
        questionsContainer.innerHTML = `<p style="color: red;">Error loading quiz: ${error.message}</p>`;
    }

    // You would integrate your QuizQuestion and ScoreDisplay components here
    // For example, if QuizQuestion.js provides a function to render a question:
    // questions.forEach(q => {
    //     questionsContainer.appendChild(renderQuizQuestion(q));
    // });
});

// A global function might be needed for inline event handlers like onclick
// Or better: use event delegation if not using a framework
window.handleAnswer = async (questionId, selectedAnswer) => {
    console.log(`Submitting answer for ${questionId}: ${selectedAnswer}`);
    // Replace 'testuser' with an actual logged-in user's username
    try {
        const result = await submitAnswer(questionId, selectedAnswer, 'testuser');
        console.log("Answer result:", result);
        alert(`Your answer was ${result.is_correct ? 'Correct' : 'Incorrect'}! XP awarded: ${result.xp_awarded}`);
    } catch (error) {
        console.error("Error submitting answer:", error);
        alert(`Error submitting answer: ${error.message}`);
    }
};

// You'll add more complex logic for quiz flow, user login/registration here