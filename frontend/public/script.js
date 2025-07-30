let username = "";
let questions = [];
let currentQuestionIndex = 0;
let totalXP = 0;

// Login for registered users
async function startSession() {
  const userInput = document.getElementById("username").value.trim();
  const passwordInput = document.getElementById("password").value.trim();

  if (!userInput || !passwordInput) {
    return alert("Enter both email and password.");
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: userInput, password: passwordInput }),
    });

    const data = await res.json();
    if (!res.ok) return alert(data.error || "Login failed");

    username = data.username;
    totalXP = data.xp || 0;

    localStorage.setItem("username", username);

    document.getElementById("login-section").classList.add("d-none");
    document.getElementById("quiz-section").classList.remove("d-none");

    await loadQuestions();
    showQuestion();
  } catch (err) {
    console.error(err);
    alert("Login error.");
  }
}

// Guest Login
async function startGuest() {
  try {
    const res = await fetch("http://127.0.0.1:5000/guest_login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });

    const data = await res.json();
    if (!res.ok) return alert(data.error || "Guest login failed");

    username = data.username;
    totalXP = data.xp || 0;

    document.getElementById("login-section").classList.add("d-none");
    document.getElementById("quiz-section").classList.remove("d-none");

    await loadQuestions();
    showQuestion();
  } catch (err) {
    console.error(err);
    alert("Guest login failed.");
  }
}

// Signup/Register new user
function signUp() {
  const userInput = document.getElementById("username").value.trim();
  const passwordInput = document.getElementById("password").value.trim();

  if (!userInput || !passwordInput) {
    return alert("Fill in email and password for sign up.");
  }

  fetch("http://127.0.0.1:5000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: userInput, password: passwordInput }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) return alert(data.error);
      alert("Registration successful. You can now log in.");
    })
    .catch((err) => {
      console.error(err);
      alert("Error during sign-up.");
    });
}

// Load Questions
async function loadQuestions() {
  try {
    const res = await fetch(`http://127.0.0.1:5000/questions?username=${username}`);
    questions = await res.json();
    currentQuestionIndex = 0;
  } catch (err) {
    alert("Failed to load questions.");
    console.error(err);
  }
}

// Show Current Question
function showQuestion() {
  const q = questions[currentQuestionIndex];
  if (!q) {
    document.getElementById("question-box").innerHTML = `<h4>🎉 You've completed the quiz!</h4>`;
    document.getElementById("answer-options").innerHTML = "";
    document.getElementById("next-btn").classList.add("d-none");
    return;
  }

  document.getElementById("question-box").innerHTML = `
    <h4>${q.text}</h4>
    <p><strong>Difficulty:</strong> ${q.difficulty} | <strong>XP:</strong> ${q.xp_value}</p>
  `;

  document.getElementById("answer-options").innerHTML = q.options.map(opt =>
    `<button class="btn btn-outline-primary w-100 mb-2 btn-option" onclick="submitAnswer('${q._id}', '${opt}')">${opt}</button>`
  ).join("");

  document.getElementById("feedback").textContent = "";
  document.getElementById("next-btn").classList.add("d-none");
}

// Submit Answer
async function submitAnswer(questionId, selectedAnswer) {
  try {
    const buttons = document.querySelectorAll('.btn-option');
    buttons.forEach(btn => btn.disabled = true);  // Disable all options on first click

    const res = await fetch("http://127.0.0.1:5000/submit_answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        question_id: questionId,
        selected_answer: selectedAnswer
      }),
    });

    const data = await res.json();
    if (data.error) throw new Error(data.error);

    totalXP += data.xp_awarded;
    document.getElementById("xp-info").textContent = `Total XP: ${totalXP}`;

    // Show feedback
    const feedbackText = data.is_correct
      ? `✅ Correct! +${data.xp_awarded} XP`
      : `❌ Incorrect. Correct answer: ${data.correct_answer}`;
    document.getElementById("feedback").textContent = feedbackText;

    // Visual feedback on buttons
    buttons.forEach(btn => {
      if (btn.textContent === data.correct_answer) {
        btn.classList.remove("btn-outline-primary");
        btn.classList.add("btn-success");
      } else if (btn.textContent === selectedAnswer && !data.is_correct) {
        btn.classList.remove("btn-outline-primary");
        btn.classList.add("btn-danger");
      }
    });

    document.getElementById("next-btn").classList.remove("d-none");
  } catch (err) {
    console.error(err);
    alert("Error submitting answer.");
  }
}

// Next Question
function nextQuestion() {
  currentQuestionIndex++;
  if (currentQuestionIndex < questions.length) {
    showQuestion();
  } else {
    document.getElementById("question-box").innerHTML = `<h4>🎉 You've completed the quiz!</h4>`;
    document.getElementById("answer-options").innerHTML = "";
    document.getElementById("next-btn").classList.add("d-none");
  }
}

// View Profile
async function viewProfile() {
  try {
    const res = await fetch(`http://127.0.0.1:5000/profile/${username}`);
    const profile = await res.json();
    if (profile.error) return alert(profile.error);

    alert(`👤 Profile of ${profile.username}\nXP: ${profile.xp}\nLevel: ${profile.level}`);
  } catch (err) {
    console.error(err);
    alert("Failed to fetch profile.");
  }
}
