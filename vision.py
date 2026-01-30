import gradio as gr

def get_vision_tab():
    with gr.TabItem("🚀 Vision & Roadmap"):
        gr.Markdown("# 🗺️ Your Journey to Full Stack AI Developer")
        gr.Markdown("Don't just learn syntax. Build a career. Here is how your small projects today turn into big skills tomorrow.")

        # Mermaid.js Diagram for the Skill Tree
        gr.Markdown("""
        ```mermaid
        graph TD
            subgraph Level 1: Beginner Portfolio
                CG[🏏 Cricket Game] -->|Teaches| Logic(🧠 Logic & Control)
                FB[🌐 Food Blog] -->|Teaches| UI(🎨 Frontend & Data)
                ET[💰 Kharcha Tracker] -->|Teaches| DB(🗄️ Database & Analysis)
                
                Logic --> Git(☁️ Git & Infra)
                UI --> Git
                DB --> Git
            end

            subgraph Level 2: The Software Architect
                Git --> Func(⚙️ Backend Modules)
                Git --> SQL(🗃️ Persistent SQL)
                Git --> CSS(🎨 Advanced Styling)
            end

            subgraph Level 3: The Full Stack Builder
                Func --> API(🔌 Fast API / Flask)
                SQL --> Auth(🔐 User Authentication)
                CSS --> React(⚛️ React / Modern UI)
            end

            subgraph Level 4: The AI Engineer
                API --> ML(🤖 ML Heuristics)
                Auth --> Scalable(🌐 Cloud Scaling)
                React --> Dashboard(📊 AI Dashboards)
            end

            style CG fill:#e1f5fe,stroke:#01579b
            style FB fill:#e8f5e9,stroke:#1b5e20
            style ET fill:#fff3e0,stroke:#e65100
            
            style Git fill:#fff9c4,stroke:#fbc02d
            
            style Logic fill:#f3e5f5,stroke:#4a148c
            style UI fill:#f3e5f5,stroke:#4a148c
            style DB fill:#f3e5f5,stroke:#4a148c
        ```
        """)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🧠 Logic Engine")
                gr.Markdown("Start with `if/else` in Cricket. End with **Machine Learning** algorithms that think like humans.")
                gr.HTML("<div style='background-color: #ddd; height: 10px; width: 100%; border-radius: 5px;'><div style='background-color: #4a148c; height: 10px; width: 10%; border-radius: 5px;'></div></div><p style='font-size: 0.8em; color: gray;'>Level: Beginner</p>")
            
            with gr.Column():
                gr.Markdown("### 🎨 Frontend UI")
                gr.Markdown("Start with `print()`. End with **Dynamic Web Apps** used by millions of people.")
                gr.HTML("<div style='background-color: #ddd; height: 10px; width: 100%; border-radius: 5px;'><div style='background-color: #1b5e20; height: 10px; width: 10%; border-radius: 5px;'></div></div><p style='font-size: 0.8em; color: gray;'>Level: Beginner</p>")
            
            with gr.Column():
                gr.Markdown("### 🗄️ Database & Memory")
                gr.Markdown("Start with `variables`. End with **Cloud Databases** that handle millions of records.")
                gr.HTML("<div style='background-color: #ddd; height: 10px; width: 100%; border-radius: 5px;'><div style='background-color: #e65100; height: 10px; width: 10%; border-radius: 5px;'></div></div><p style='font-size: 0.8em; color: gray;'>Level: Beginner</p>")

        gr.Markdown("---")
        gr.Markdown("### 🏁 Level 1 Outcomes: The Junior Builder")
        gr.Markdown("- **Console Games** with logical decision trees.")
        gr.Markdown("- **Web Page Generators** that automate UI creation.")
        gr.Markdown("- **Data Analyzers** that manage files and calculate spend.")
        gr.Markdown("- **Git Mastery** to track and share every line of code.")