let questions = [];
let testQuestions = [];

let currentQuestion = 0;
let selectedAnswer = null;
let score = 0;

const questionElement =
    document.getElementById("question");

const optionButtons =
    document.querySelectorAll(".option");

const submitButton =
    document.getElementById("submitBtn");

const resultElement =
    document.getElementById("result");

const explanationElement =
    document.getElementById("explanation");


// ==========================================
// Load all questions from backend
// ==========================================

async function loadQuestions() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/questions"
        );

        questions = await response.json();

        startNewTest();

    } catch (error) {

        resultElement.textContent =
            "Unable to load questions.";

        console.error(error);
    }
}


// ==========================================
// Start a new test
// ==========================================

function startNewTest() {

    testQuestions = [...questions]
        .sort(() => Math.random() - 0.5)
        .slice(0, 10);

    currentQuestion = 0;

    score = 0;

    optionButtons.forEach(button => {

        button.style.display = "block";

        button.disabled = false;

    });

    submitButton.style.display =
        "inline-block";

    submitButton.disabled = false;

    showQuestion();
}


// ==========================================
// Display current question
// ==========================================

function showQuestion() {

    const current =
        testQuestions[currentQuestion];

    questionElement.textContent =
        `Question ${currentQuestion + 1} of 10: ${current.question}`;


    optionButtons.forEach(
        (button, index) => {

            const optionLetter =
                String.fromCharCode(65 + index);

            button.textContent =
                `${optionLetter}. ${current.options[index]}`;

            button.style.background =
                "white";

            button.disabled = false;

            button.style.display =
                "block";

        }
    );


    selectedAnswer = null;

    resultElement.textContent = "";

    explanationElement.textContent = "";

    submitButton.style.display =
        "inline-block";

    submitButton.disabled = false;
}


// ==========================================
// Select an answer
// ==========================================

optionButtons.forEach(
    (button, index) => {

        button.addEventListener(
            "click",
            () => {

                selectedAnswer =
                    index;

                optionButtons.forEach(
                    btn => {

                        btn.style.background =
                            "white";

                    }
                );

                button.style.background =
                    "#e0e0e0";

            }
        );

    }
);


// ==========================================
// Submit answer
// ==========================================

submitButton.addEventListener(
    "click",
    async () => {

        if (selectedAnswer === null) {

            resultElement.textContent =
                "Please select an answer.";

            return;
        }


        // Prevent multiple clicks

        submitButton.disabled = true;


        try {

            const questionIndex =
                questions.indexOf(
                    testQuestions[currentQuestion]
                );


            const response =
                await fetch(
                    "http://127.0.0.1:8000/check-answer",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            question_index:
                                questionIndex,

                            answer_index:
                                selectedAnswer

                        })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Server error: ${response.status}`
                );

            }


            const result =
                await response.json();


            if (result.correct) {

                score++;

                resultElement.textContent =
                    "✅ Correct Answer!";

            } else {

                resultElement.textContent =
                    "❌ Wrong Answer!";

            }


            explanationElement.textContent =
                "Correct Answer: " +
                result.correct_answer;


            // Disable options after submitting

            optionButtons.forEach(
                button => {

                    button.disabled = true;

                }
            );


            submitButton.style.display =
                "none";


            // Remove old next button if any

            const oldNextButton =
                document.getElementById(
                    "nextButton"
                );


            if (oldNextButton) {

                oldNextButton.remove();

            }


            // Create Next Question button

            const nextButton =
                document.createElement(
                    "button"
                );


            nextButton.textContent =
                currentQuestion === 9
                    ? "View Result"
                    : "Next Question";


            nextButton.id =
                "nextButton";


            nextButton.style.marginTop =
                "20px";

            nextButton.style.padding =
                "12px 25px";

            nextButton.style.border =
                "none";

            nextButton.style.borderRadius =
                "6px";

            nextButton.style.background =
                "#333";

            nextButton.style.color =
                "white";

            nextButton.style.cursor =
                "pointer";


            document
                .querySelector(".quiz-box")
                .appendChild(
                    nextButton
                );


            nextButton.addEventListener(
                "click",
                () => {

                    nextButton.remove();

                    currentQuestion++;


                    if (
                        currentQuestion < 10
                    ) {

                        showQuestion();

                    } else {

                        showFinalResult();

                    }

                }
            );


        } catch (error) {

            console.error(error);

            resultElement.textContent =
                "Something went wrong. Please try again.";

            submitButton.disabled =
                false;

        }

    }
);


// ==========================================
// Save test result to MongoDB
// ==========================================

async function saveTestResult() {

    const testResult =
        score >= 5
            ? "PASS"
            : "FAIL";


    // Get logged-in student's username

    const studentName =
        localStorage.getItem(
            "student_name"
        );


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/save-result",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        // Save the logged-in user's name
                        student_name:
                            studentName || "Student",

                        score:
                            score,

                        total_questions:
                            10,

                        result:
                            testResult

                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            data.message
        );


    } catch (error) {

        console.error(
            "Unable to save test result:",
            error
        );

    }
}


// ==========================================
// Show final result
// ==========================================

async function showFinalResult() {

    questionElement.textContent =
        "🎉 Test Completed!";


    optionButtons.forEach(
        button => {

            button.style.display =
                "none";

        }
    );


    resultElement.textContent =
        `Your Score: ${score}/10`;


    if (score >= 5) {

        explanationElement.textContent =
            "🎉 PASS! Congratulations!";

    } else {

        explanationElement.textContent =
            "❌ FAIL — Better Luck Next Time! 😊";

    }


    submitButton.style.display =
        "none";


    // ==========================================
    // Save result to MongoDB
    // ==========================================

    await saveTestResult();


    // ==========================================
    // Create Start Next Test button
    // ==========================================

    const nextTestButton =
        document.createElement(
            "button"
        );


    nextTestButton.textContent =
        "Start Next Test";


    nextTestButton.id =
        "nextTestButton";


    nextTestButton.style.marginTop =
        "20px";

    nextTestButton.style.padding =
        "12px 25px";

    nextTestButton.style.border =
        "none";

    nextTestButton.style.borderRadius =
        "6px";

    nextTestButton.style.background =
        "#333";

    nextTestButton.style.color =
        "white";

    nextTestButton.style.cursor =
        "pointer";


    document
        .querySelector(".quiz-box")
        .appendChild(
            nextTestButton
        );


    nextTestButton.addEventListener(
        "click",
        () => {

            nextTestButton.remove();


            optionButtons.forEach(
                button => {

                    button.style.display =
                        "block";

                }
            );


            startNewTest();

        }
    );

}


// ==========================================
// Start application
// ==========================================

loadQuestions();