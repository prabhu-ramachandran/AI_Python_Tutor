import gradio as gr
from database import get_user_progress
import json

def calculate_xp(username):
    if not username:
        return {"Logic": 5, "Frontend": 5, "Database": 5} # Default 5% for visualization
    
    progress = get_user_progress(username)
    if not progress or "completed" not in progress:
        return {"Logic": 5, "Frontend": 5, "Database": 5}
    
    completed = progress["completed"] # Dict of {mod_name: metrics}
    
    # XP Counters
    logic = 0
    frontend = 0
    db = 0
    
    for mod_name in completed.keys():
        m = mod_name.lower()
        if "logic" in m or "loop" in m or "condition" in m or "umpire" in m or "auditor" in m:
            logic += 1
        if "menu" in m or "html" in m or "string" in m or "ui" in m or "stadium" in m:
            frontend += 1
        if "variable" in m or "list" in m or "dictionary" in m or "csv" in m or "wallet" in m or "ledger" in m:
            db += 1
            
    # Normalize (Assuming ~5 modules per skill for Level 1)
    return {
        "Logic": min(logic * 20, 100), 
        "Frontend": min(frontend * 20, 100), 
        "Database": min(db * 20, 100)
    }

def get_vision_tab(request = None):
    # Calculate XP based on user
    username = request.username if request else None
    xp = calculate_xp(username)
    
    logic_pct = xp["Logic"]
    ui_pct = xp["Frontend"]
    db_pct = xp["Database"]

    with gr.TabItem("🚀 Vision & Roadmap"):
        gr.Markdown("# 🗺️ Your Journey to Full Stack AI Developer")
        gr.Markdown("Don't just learn syntax. Build a career. Here is how your small projects today turn into big skills tomorrow.")

        # Mermaid.js Diagram for the Skill Tree
        gr.Markdown("""
        ```mermaid
        %%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#1f2937', 'edgeLabelBackground':'#111827', 'tertiaryColor': '#111827'}}}%%
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

            style CG fill:#0d47a1,stroke:#e1f5fe,color:white
            style FB fill:#1b5e20,stroke:#e8f5e9,color:white
            style ET fill:#e65100,stroke:#fff3e0,color:white
            
            style Git fill:#fbc02d,stroke:#fff9c4,color:black
            
            style Logic fill:#4a148c,stroke:#f3e5f5,color:white
            style UI fill:#4a148c,stroke:#f3e5f5,color:white
            style DB fill:#4a148c,stroke:#f3e5f5,color:white
        ```
        """)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🧠 Logic Engine")
                gr.Markdown("Start with `if/else` in Cricket. End with **Machine Learning** algorithms that think like humans.")
                gr.HTML(f"<div style='background-color: #ddd; height: 10px; width: 100%; border-radius: 5px;'><div style='background-color: #4a148c; height: 10px; width: {logic_pct}%; border-radius: 5px;'></div></div><p style='font-size: 0.8em; color: gray;'>Level: {logic_pct}%</p>")
            
            with gr.Column():
                gr.Markdown("### 🎨 Frontend UI")
                gr.Markdown("Start with `print()`. End with **Dynamic Web Apps** used by millions of people.")
                gr.HTML(f"<div style='background-color: #ddd; height: 10px; width: 100%; border-radius: 5px;'><div style='background-color: #1b5e20; height: 10px; width: {ui_pct}%; border-radius: 5px;'></div></div><p style='font-size: 0.8em; color: gray;'>Level: {ui_pct}%</p>")
            
            with gr.Column():
                gr.Markdown("### 🗄️ Database & Memory")
                gr.Markdown("Start with `variables`. End with **Cloud Databases** that handle millions of records.")
                gr.HTML(f"<div style='background-color: #ddd; height: 10px; width: 100%; border-radius: 5px;'><div style='background-color: #e65100; height: 10px; width: {db_pct}%; border-radius: 5px;'></div></div><p style='font-size: 0.8em; color: gray;'>Level: {db_pct}%</p>")

        gr.Markdown("---")
        gr.Markdown("### 🏁 Level 1 Outcomes: The Junior Builder")
        gr.Markdown("- **Console Games** with logical decision trees.")
        gr.Markdown("- **Web Page Generators** that automate UI creation.")
        gr.Markdown("- **Data Analyzers** that manage files and calculate spend.")
        gr.Markdown("- **Git Mastery** to track and share every line of code.")