# Twtr Post Generator

An agentic AI application built with **LangGraph** and **Groq LLMs** that generates, evaluates, and optimizes engaging X (Twitter) posts through an iterative multi-agent workflow.

---

# Features

- AI-powered X post generation
- Multi-agent architecture using LangGraph
- Generator Agent creates an initial post
- Evaluator Agent reviews quality and provides feedback
- Optimizer Agent rewrites the post based on feedback
- Automatic refinement until the post is approved or the maximum number of iterations is reached
- Powered by Groq LLMs

---

# Workflow

```text
            Topic
              │
              ▼
      Generator Agent
              │
              ▼
      Evaluator Agent
              │
      Approved?
      ┌─────────────┐
      │             │
     Yes           No
      │             │
      ▼             ▼
 Final Output  Optimizer Agent
                    │
                    ▼
             Evaluator Agent
```

---

# Tech Stack

- Python
- LangGraph
- LangChain
- Groq API
- Pydantic

---

# Project Structure

```text
Twtr_post_generator/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/granthx/Twtr_post_generator.git
cd Twtr_post_generator
```

## Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure environment variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Running the Project

```bash
python main.py
```

Example

```text
Enter Topic:
Artificial Intelligence
```

The application will:

1. Generate an X post.
2. Evaluate the generated post.
3. Optimize the post if needed.
4. Repeat until the evaluator approves it or the maximum iteration limit is reached.

---

# Agent Architecture

## Generator Agent

Responsible for generating the initial X post based on the provided topic.

## Evaluator Agent

Evaluates the generated post using multiple quality criteria including:

- Originality
- Hook
- Clarity
- Engagement
- Authenticity
- Readability

Provides detailed feedback and determines whether the post should be approved or improved.

## Optimizer Agent

Uses the evaluator's feedback to improve the post while preserving its original intent.

---

# Example Workflow

```text
Topic
    │
    ▼
Generate Post
    │
    ▼
Evaluate
    │
    ├── Approved
    │       │
    │       ▼
    │   Final Output
    │
    └── Needs Improvement
            │
            ▼
      Optimize Post
            │
            ▼
       Evaluate Again
```

---

# Future Improvements

- Streamlit web interface
- Multiple writing styles
- AI-generated hashtags
- Trending topic integration
- Memory-enabled agents
- Social media analytics
- Multi-platform support (LinkedIn, Threads, Bluesky)

---

# Contributing

Contributions are welcome.

Feel free to fork the repository, create a feature branch, and submit a pull request.

---

# License

This project is licensed under the MIT License.

---

# Author

**Granth Chhabra**

GitHub: https://github.com/granthx

LinkedIn: https://www.linkedin.com/in/granthchhabra/
