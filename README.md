# Simple LLM Chatbot

A small Python Flask app with an HTML, CSS, and JavaScript chat UI.

## Setup

1. Open this folder in your IDE:

```powershell
C:\Users\theed\CascadeProjects\simple-llm-chatbot
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file by copying `.env.example`, then add your OpenAI API key:

```powershell
Copy-Item .env.example .env
```

5. Set your API key in `.env`:

```text
OPENAI_API_KEY=your_real_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Run

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Notes

- Do not commit your `.env` file.
- The backend reads `OPENAI_API_KEY` from your environment.
- You can change the model with `OPENAI_MODEL`.
