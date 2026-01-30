import gradio as gr

def get_vision_tab():
    with gr.TabItem("🚀 Vision & Roadmap"):
        gr.Markdown("# 🗺️ Your Journey to Full Stack AI Developer")
        gr.Markdown("Don't just learn syntax. Build a career. Here is how your small projects today turn into big skills tomorrow.")

        # Mermaid.js Diagram for the Skill Tree
        gr.Markdown("""
        ```mermaid
        graph TD
            subgraph Level 1: The Foundation
                CG[🏏 Cricket Game] -->|Teaches| Logic(🧠 Logic)
                FB[🌐 Food Blog] -->|Teaches| UI(🎨 Frontend)
                ET[💰 Expense Tracker] -->|Teaches| DB(🗄️ Database)
            end

            subgraph Level 2: The Architect
                Logic --> Func(⚙️ Functions & Modules)
                UI --> Jinja(📄 Templating)
                DB --> SQL(🗃️ SQLite/Postgres)
            end

            subgraph Level 3: The Builder
                Func --> API(🔌 REST APIs)
                Jinja --> WebApp(🌍 Flask/FastAPI)
                SQL --> UserData(busts Persistent User Data)
            end

            subgraph Level 4: The AI Engineer
                API --> Bot(🤖 AI Game Bot)
                WebApp --> Deploy(☁️ Cloud Deployment)
                UserData --> Insights(bR Smart Analytics)
            end

            style CG fill:#e1f5fe,stroke:#01579b
            style FB fill:#e8f5e9,stroke:#1b5e20
            style ET fill:#fff3e0,stroke:#e65100
            
            style Logic fill:#f3e5f5,stroke:#4a148c
            style UI fill:#f3e5f5,stroke:#4a148c
            style DB fill:#f3e5f5,stroke:#4a148c
        ```
        """)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🧠 Logic Engine")
                gr.Markdown("Start with `if/else` in Cricket. End with **Machine Learning** algorithms that beat humans.")
                gr.Progress(value=0.1, label="Current Level: Beginner")
            
            with gr.Column():
                gr.Markdown("### 🎨 Frontend UI")
                gr.Markdown("Start with `print()`. End with **React/Dashboard** interfaces used by millions.")
                gr.Progress(value=0.1, label="Current Level: Beginner")
            
            with gr.Column():
                gr.Markdown("### 🗄️ Database & Memory")
                gr.Markdown("Start with `variables`. End with **Big Data** systems that handle millions of records.")
                gr.Progress(value=0.1, label="Current Level: Beginner")

        gr.Markdown("---")
        gr.Markdown("### 🏆 Final Goal: The 'Bangalore Tech Stack' Certification")
        gr.Markdown("By the end of this course, you will have a portfolio with a Game, a Website, and a Financial Tool, all built by YOU.")
