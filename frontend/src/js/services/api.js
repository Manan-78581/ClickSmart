// frontend/src/js/services/api.js

const API_BASE_URL = 'http://127.0.0.1:5000'; // Your Flask Backend URL

/**
 * Fetches all questions from the backend.
 * @returns {Promise<Array>} A promise that resolves to an array of question objects.
 */
export async function getQuestions() {
    try {
        const response = await fetch(`${API_BASE_URL}/questions`);
        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`Failed to fetch questions: ${response.status} - ${errorBody}`);
        }
        const questions = await response.json();
        return questions;
    } catch (error) {
        console.error("Error in getQuestions:", error);
        throw error; // Re-throw to be handled by the caller
    }
}

/**
 * Registers a new user.
 * @param {string} username
 * @param {string} password
 * @returns {Promise<Object>} A promise that resolves to the registration response.
 */
export async function registerUser(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to register user');
        }
        return data;
    } catch (error) {
        console.error("Error in registerUser:", error);
        throw error;
    }
}

/**
 * Logs in a user.
 * @param {string} username
 * @param {string} password
 * @returns {Promise<Object>} A promise that resolves to the login response.
 */
export async function loginUser(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to login user');
        }
        return data;
    } catch (error) {
        console.error("Error in loginUser:", error);
        throw error;
    }
}

/**
 * Submits a user's answer to a question.
 * @param {string} questionId
 * @param {string} selectedAnswer
 * @param {string} username // Assuming username is sent for XP tracking
 * @returns {Promise<Object>} A promise that resolves to the answer submission response.
 */
export async function submitAnswer(questionId, selectedAnswer, username) {
    try {
        const response = await fetch(`${API_BASE_URL}/submit_answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question_id: questionId, selected_answer: selectedAnswer, username: username })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to submit answer');
        }
        return data;
    } catch (error) {
        console.error("Error in submitAnswer:", error);
        throw error;
    }
}

/**
 * Gets a user's profile information (XP, level).
 * @param {string} username
 * @returns {Promise<Object>} A promise that resolves to the user's profile data.
 */
export async function getUserProfile(username) {
    try {
        const response = await fetch(`${API_BASE_URL}/profile/${username}`);
        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`Failed to fetch user profile: ${response.status} - ${errorBody}`);
        }
        const profile = await response.json();
        return profile;
    } catch (error) {
        console.error("Error in getUserProfile:", error);
        throw error;
    }
}