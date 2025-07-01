# 🤖 Code Correct: Your Intelligent AI Programming Assistant 🚀

## ✨ Fix Code, Understand Concepts, Troubleshoot Software ✨

![Code Correct Screenshot Placeholder](https://placehold.co/800x400/282c34/E0E0E0?text=Code+Correct+App+Screenshot)

---

### Introduction

**Code Correct** is an innovative AI-powered chatbot designed to be your ultimate companion in the world of programming and software development. Built with Streamlit and powered by Google's Gemini API, this application provides instant, intelligent assistance for debugging code, answering complex programming questions, and even troubleshooting PC software issues.

Say goodbye to endless Stack Overflow searches and frustrating debugging sessions. Code Correct is here to streamline your workflow and enhance your understanding, helping you write cleaner, more efficient code and keep your development environment running smoothly.

---

### Key Features 🌟

* **Intelligent Code Correction & Debugging:** 🐛🛠️💡
    * Submit your code snippets, and Code Correct will identify errors, suggest fixes, and provide the corrected code.
    * Receive detailed, step-by-step explanations of *why* the error occurred and *how* it was resolved, fostering a deeper understanding of programming concepts.
    * Get recommendations for best practices, code optimization, and adherence to coding standards.

* **Comprehensive Programming Q&A:** ❓📚🧠
    * Ask any question related to programming languages, algorithms, data structures, software design patterns, specific libraries, frameworks, or development methodologies.
    * Receive clear, accurate, and comprehensive answers, often accompanied by illustrative code examples.

* **PC Software Troubleshooting:** 💻🩺⚙️
    * Describe software problems you're facing on your personal computer (e.g., application crashes, driver issues, OS errors).
    * Code Correct will diagnose potential causes and provide actionable, step-by-step troubleshooting guides to help you resolve the issues.

* **Context-Aware & Focused:** 🎯🧠
    * The AI is specifically engineered to stay within the domain of programming, coding, and software troubleshooting.
    * Politely redirects out-of-context queries, ensuring a focused and efficient problem-solving experience.

* **Aesthetically Pleasing & User-Friendly Interface:** ✨🎨📱
    * A clean, modern interface built with Streamlit.
    * Custom CSS for a visually appealing dark theme with a subtle background image.
    * Bolder, more visible input fields for enhanced usability.

---

### Why Code Correct? 🤔

* **Boost Productivity:** ⚡🚀 Get instant answers and solutions, reducing time spent on debugging and research.

* **Learn & Grow:** 🌱🎓 Detailed explanations help you understand underlying concepts, turning debugging into a learning opportunity.

* **Reliable Assistance:** ✅🛡️ Powered by a robust AI model and guided by expert prompt engineering techniques (Chain of Thought, Guardrails, Few-Shot learning).

* **All-in-One Solution:** 📦🌐 From syntax errors to software glitches, get comprehensive support in one place.

---

### Getting Started 🚀

Follow these steps to set up and run Code Correct on your local machine.

#### Prerequisites ✅

* Python 3.8+
* `pip` (Python package installer)
* A Google Cloud Project with the Gemini API enabled.
* A Gemini API Key.

#### 1. Clone the Repository ⬇️📂

First, clone this repository to your local machine:

```bash
git clone [https://github.com/your-username/code_correct.git](https://github.com/your-username/code_correct.git)
cd code_correct/src
```
*(Replace `https://github.com/your-username/code_correct.git` with your actual repository URL)*

### 2. Create a Virtual Environment (Recommended) 🐍📦

It's good practice to use a virtual environment to manage dependencies:

```bash
python -m venv venv
```

* **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
* **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies ⚙️📦

Navigate into the `src` directory (where `app.py` and `requirements.txt` are located) and install the necessary libraries:

```bash
cd src
pip install -r requirements.txt
```

Your `requirements.txt` should be clean and minimal, like this:

```
streamlit
google-generativeai
firebase-admin
google-cloud-firestore
```
*(Ensure your `requirements.txt` matches this clean version to avoid deployment issues.)*

### 4. Set Up Your Gemini API Key 🔑🔒

Streamlit can securely manage your API keys using `secrets.toml`.

Create a `.streamlit` folder in the root of your project (the `code_correct` directory, *not* inside `src`). Inside `.streamlit`, create a file named `secrets.toml` with your Gemini API key:

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```
*(Replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key.)*

Alternatively, you can set it as an environment variable: `GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"`.

### 5. Place Your Prompt File 📝🧠

Ensure you have a `prompt.txt` file in the `src` directory, containing the refined prompt for the AI's behavior. For example, using the "Balanced Edition" prompt we developed:

```
# prompt.txt content
You are "Code Correct," an expert AI for all things programming, coding, debugging, and PC software troubleshooting. Your core purpose is to provide clear, accurate, and actionable solutions exclusively within these domains.

### Core Capabilities & Approach:

* **Code Correction & Explanation:** When given code, you'll **fix it**, then provide a **step-by-step breakdown** of the problem, its cause, and the exact solution. Your explanations will be educational, akin to a mentor guiding a student.
* **Programming Q&A:** Answer any question about programming concepts, languages, algorithms, data structures, and best practices. Explain clearly, using examples where helpful.
* **PC Software Troubleshooting:** Diagnose user-reported PC software issues (e.g., application errors, OS problems) and provide **actionable troubleshooting steps** and potential solutions.

### Prompt Engineering Directives:

1.  **Chain of Thought (Internal):** For every task, you'll internally analyze the problem (code errors, user questions, software symptoms), diagnose the root cause, determine the optimal solution, and then structure a logical, step-by-step explanation for the user.
2.  **Few-Shot (Learned Patterns):** You've absorbed thousands of successful code fixes, clear programming explanations, and effective troubleshooting flows. Apply these learned patterns to new, similar problems.
3.  **Guardrails (Context Specificity):**
    * **Strict Domain:** Your expertise is **solely** programming, coding, debugging, and PC software.
    * **Out-of-Context Handling:** If a user's query falls outside this scope, respond politely but firmly: "I specialize in programming, coding, and software troubleshooting. Please ask me a question related to those topics, and I'll be happy to help!"
    * **Clarification:** If a request is unclear or lacks detail, ask precise questions to get the necessary information (e.g., "Please provide the code snippet and any error messages").
4.  **Tone & Formatting:** Maintain an **expert, helpful, and educational** tone. Use **code blocks** for code, **bolding** for keywords, and **bullet points/numbered lists** for steps to ensure maximum readability and clarity.
```

### 6. Add Your Background Image 🖼️🎨

Place your desired background image file (e.g., `background.jpg`, `bg_image.png`) directly into the `src` directory alongside `app.py`. Then, open `app.py` and update this line in the CSS:

```python
# In app.py, within the <style> tag:
background-image: url("your_background_image.jpg"); # Replace with your image filename
```

### 7. Run the Application ▶️🚀

With your virtual environment activated and all files in place, run the Streamlit app from the `src` directory:

```bash
streamlit run app.py
```

Your browser should automatically open to the Code Correct AI Chatbot!

---

### Project Structure 📁

```
code_correct/
├── .streamlit/
│   └── secrets.toml         # Securely stores your Gemini API Key
├── src/
│   ├── app.py               # The main Streamlit application
│   ├── prompt.txt           # Contains the AI's core instructions/prompt
│   └── your_background_image.jpg # Your chosen background image
├── requirements.txt         # Lists Python dependencies
└── README.md                # This file
```

---

### Customization 🔧

* **AI Prompt:** Modify `prompt.txt` to fine-tune the AI's behavior and responses.
* **Background:** Change `your_background_image.jpg` in `src` and update the `url()` in `app.py`'s CSS.
* **Styling:** Adjust the CSS within `app.py` to change colors, fonts, and layout.
* **Gemini Model:** Experiment with different Gemini models (e.g., `gemini-1.5-pro`) by changing `model = genai.GenerativeModel('gemini-1.5-flash')` in `app.py`.

---

Made by BigMO (Mo-Dev)
