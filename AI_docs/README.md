# AI Python Tutor Project: Goal & Vision

## 🎯 Project Goal
To provide a high-quality, interactive, and inclusive Python learning experience for students in Bangalore, India, by leveraging AI. This platform moves away from static lessons and embraces a **Socratic Learning Model** where the AI acts as a guide, asking questions and providing hints rather than just giving answers.

## 🏗️ Technical Architecture
- **Frontend:** Gradio (for rapid, Python-based UI development).
- **Orchestration:** LangGraph (Agent SDK) to manage conversation state and learning logic.
- **LLM:** Google Gemini 2.0 (for high-speed reasoning).
- **Environment:** Python 3.x with a virtual environment (`venv`).

## 🛠️ CLI Operations (Cheat Sheet)
- **Activate Environment:** `source venv/bin/activate`
- **Run the Application:** `python app.py`
- **Install New Tools:** `pip install <package_name>`
- **Add Lessons:** Edit `logic.py` or add new configuration to the `modules/` directory.

## 🌟 Key Principles
1. **Zero Knowledge Start:** Assume the student has never seen a line of code.
2. **Interactive Only:** No walls of text. Education happens through feedback loops.
3. **Local Context:** Use Bangalore-specific analogies (Cricket at Chinnaswamy, Silk Board Traffic, Namma Metro, Commercial Street shopping) to make concepts relatable.
4. **Agentic Logic:** Use the Agent SDK to allow the AI to 'step back' and think about the student's progress before responding.

## 🚀 Next Steps
- **Sandbox Integration:** Add a code execution window using `gr.Code()`.
- **Dynamic Curriculum:** Expand the module list in `app.py`.
- **Persistence:** Implement user progress tracking in a local SQLite database.