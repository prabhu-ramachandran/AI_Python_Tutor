import gradio as gr
from database import get_user_progress

def calculate_xp(username):
    if not username or username == "guest":
        return {"Logic": 5, "Frontend": 5, "Database": 5}
    
    progress = get_user_progress(username)
    if not progress or "completed" not in progress:
        return {"Logic": 5, "Frontend": 5, "Database": 5}
    
    completed = progress["completed"]
    logic = 0
    frontend = 0
    db = 0
    for mod_name in completed.keys():
        m = mod_name.lower()
        if any(x in m for x in ["logic", "loop", "condition", "umpire", "auditor"]):
            logic += 1
        if any(x in m for x in ["menu", "html", "string", "ui", "stadium"]):
            frontend += 1
        if any(x in m for x in ["variable", "list", "dictionary", "csv", "wallet", "ledger"]):
            db += 1
            
    return {
        "Logic": min(logic * 20, 100), 
        "Frontend": min(frontend * 20, 100), 
        "Database": min(db * 20, 100)
    }

def get_xp_html(label, pct, color):
    return f"""
    <div style='margin-bottom: 10px;'>
        <div style='background-color: #ddd; height: 10px; width: 100%; border-radius: 5px;'>
            <div style='background-color: {color}; height: 10px; width: {pct}%; border-radius: 5px;'></div>
        </div>
        <p style='font-size: 0.8em; color: gray; margin: 0;'>Level: {pct}%</p>
    </div>
    """

def get_vision_tab():
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
                logic_bar = gr.HTML(get_xp_html("Logic", 5, "#4a148c"))
            
            with gr.Column():
                gr.Markdown("### 🎨 Frontend UI")
                ui_bar = gr.HTML(get_xp_html("Frontend", 5, "#1b5e20"))
            
            with gr.Column():
                gr.Markdown("### 🗄️ Database & Memory")
                db_bar = gr.HTML(get_xp_html("Database", 5, "#e65100"))

        gr.Markdown("---")
        gr.Markdown("### 🏁 Level 1 Outcomes: The Junior Builder")
        gr.Markdown("- **Console Games** with logical decision trees.")
        gr.Markdown("- **Web Page Generators** that automate UI creation.")
        gr.Markdown("- **Data Analyzers** that manage files and calculate spend.")
        gr.Markdown("- **Git Mastery** to track and share every line of code.")
        
    return logic_bar, ui_bar, db_bar
