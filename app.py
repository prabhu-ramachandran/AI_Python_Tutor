import gradio as gr
from logic import socratic_agent
from langchain_core.messages import HumanMessage, AIMessage
from vision import get_vision_tab

def chat_with_tutor(message, history, module_name, goal_name):
    # Convert history for the Agent
    formatted_history = []
    
    # Handle Gradio's new "messages" format (list of dicts)
    for msg in history:
        if msg['role'] == 'user':
            formatted_history.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            formatted_history.append(AIMessage(content=msg['content']))
    
    # Run the Agent
    input_state = {
        "messages": formatted_history + [HumanMessage(content=message)],
        "module_name": module_name,
        "goal": goal_name
    }
    
    result = socratic_agent.invoke(input_state)
    return result["messages"][-1].content

# Curriculum Definitions
CURRICULUM = {
    "Cricket Game": [
        "The Stadium (I/O)",
        "The Scoreboard (Variables)",
        "The Umpire (Conditionals)",
        "The Over (Loops)",
        "The Commentary (Functions)",
        "Match Recap (Git)"
    ],
    "Food Blog": [
        "The Menu (Strings)",
        "The Foodies List (Lists)",
        "Hotel Cards (Dictionaries)",
        "The Generator (Loops)",
        "Go Live (File I/O)",
        "Cloud Launch (Infra)"
    ],
    "Expense Tracker": [
        "The Wallet (Data Types)",
        "Daily Ledger (CSV)",
        "App Menu (Flow)",
        "The Auditor (Logic)",
        "The Workshop (Infra)",
        "Portfolio (Final)"
    ]
}

# UI Layout
with gr.Blocks(title="Bengaluru AI Tutor", theme=gr.themes.Soft()) as demo:
    with gr.Row():
        gr.Markdown("# 🏫 Bengaluru AI Code Lab")
        login_btn = gr.LoginButton()

    # State Management
    current_view = gr.State("selection")
    selected_goal = gr.State(None)
    selected_mod = gr.State("Intro")

    # This column will only be visible if the user is logged in
    with gr.Column(visible=False) as main_container:
        with gr.Tabs():
            with gr.TabItem("🎓 Classroom"):
                # --- VIEW 1: Goal Selection (Beginner Level) ---
                with gr.Column(visible=True) as welcome_screen:
                    gr.Markdown("## 👋 Namaskara! What do you want to build first?")
                    gr.Markdown("Choose your **Beginner Level** project. We will learn Python step-by-step to build this.")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 🏏 Gully Cricket Game")
                            gr.Markdown("Build a text game where you bat against the computer.")
                            btn_cricket = gr.Button("Choose Cricket 🏏", variant="primary")
                        
                        with gr.Column():
                            gr.Markdown("### 🌐 Food Blog Generator")
                            gr.Markdown("Create a tool to make a website for your favorite hotels.")
                            btn_blog = gr.Button("Choose Food Blog 🌐", variant="primary")
                        
                        with gr.Column():
                            gr.Markdown("### 💰 Kharcha Tracker")
                            gr.Markdown("Build an app to track your daily expenses (Auto, Coffee, etc).")
                            btn_finance = gr.Button("Choose Expense Tracker 💰", variant="primary")

                # --- VIEW 2: The Classroom (Tutor Interface) ---
                with gr.Column(visible=False) as tutor_screen:
                    with gr.Row():
                        btn_back = gr.Button("⬅️ Back to Goals", size="sm")
                        goal_display = gr.Markdown("Current Goal: ...")

                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### 🗺️ Your Path")
                            # Placeholder buttons for the curriculum
                            m1 = gr.Button("1. Module")
                            m2 = gr.Button("2. Module")
                            m3 = gr.Button("3. Module")
                            m4 = gr.Button("4. Module")
                            m5 = gr.Button("5. Module")
                            m6 = gr.Button("6. Module")

                            gr.Markdown("### 🔒 Level 2 (Locked)")
                            gr.Button("7. Advanced Engineering", interactive=False)
                            
                        with gr.Column(scale=3):
                            chatbot_comp = gr.Chatbot(label="Socratic Tutor", type="messages")
                            with gr.Row():
                                txt_input = gr.Textbox(show_label=False, placeholder="Type your answer here...", scale=4)
                                btn_submit = gr.Button("Send ➤", scale=1)
            
            # Add the Vision Tab
            get_vision_tab()

    # Message to show when not logged in
    with gr.Column(visible=True) as login_prompt:
        gr.Markdown("### Please sign in to start your learning journey! 🚀")
        gr.Markdown("We use Hugging Face login (which supports Google/Gmail) to save your progress safely.")

    # --- Logic for Login Handling ---
    def check_user(request):
        print(f"--- Login Check ---")
        if request:
            print(f"Request detected. Username: {request.username}")
        else:
            print("No request object detected.")

        if request and request.username:
            try:
                # Auto-register user if new
                ensure_user_exists(request.username)
                print(f"User {request.username} verified in database.")
            except Exception as e:
                print(f"Database error during login: {e}")
            
            return gr.update(visible=True), gr.update(visible=False)
        
        print("Redirecting to login prompt.")
        return gr.update(visible=False), gr.update(visible=True)

    demo.load(check_user, None, [main_container, login_prompt], api_name=False)

    # --- Chat Logic with Side Effects ---
    def submit_message(user_text, history, module_name, goal_name, request):
        if not user_text.strip():
            return {txt_input: gr.update()}

        new_history = history + [{"role": "user", "content": user_text}]
        
        formatted_history = []
        for msg in new_history:
            if msg['role'] == 'user':
                formatted_history.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                formatted_history.append(AIMessage(content=msg['content']))

        input_state = {
            "messages": formatted_history,
            "module_name": module_name,
            "goal": goal_name
        }
        result = socratic_agent.invoke(input_state)
        ai_response = result["messages"][-1].content
        
        updated_mod_state = module_name
        
        if "[MODULE_COMPLETE]" in ai_response:
            ai_response = ai_response.replace("[MODULE_COMPLETE]", "").strip()
            ai_response += "\n\n🎉 **Module Complete! Unlocking the next level...**"
            
            modules = CURRICULUM[goal_name]
            try:
                current_idx = -1
                for i, m in enumerate(modules):
                    if m == module_name:
                        current_idx = i
                        break
                
                if current_idx != -1 and current_idx < len(modules) - 1:
                    updated_mod_state = modules[current_idx + 1]
                    
                    # SAVE PROGRESS TO DB
                    if request and request.username:
                        steps_taken = len(new_history) // 2
                        metrics = {
                            "completed_module_name": module_name,
                            "steps": steps_taken
                        }
                        save_progress(request.username, goal_name, updated_mod_state, metrics)
            except Exception as e:
                print(f"Error saving progress: {e}")
                pass

        final_history = new_history + [{"role": "assistant", "content": ai_response}]
        
        return {
            chatbot_comp: final_history,
            txt_input: "",
            selected_mod: updated_mod_state
        }

    # Wire up the Custom Chat
    txt_input.submit(
        submit_message, 
        [txt_input, chatbot_comp, selected_mod, selected_goal], 
        [chatbot_comp, txt_input, selected_mod],
        api_name=False
    )
    btn_submit.click(
        submit_message, 
        [txt_input, chatbot_comp, selected_mod, selected_goal], 
        [chatbot_comp, txt_input, selected_mod],
        api_name=False
    )

    # --- Logic for View Switching ---
    def start_course(goal):
        modules = CURRICULUM[goal]
        first_mod = modules[0]
        
        initial_input = {
            "messages": [HumanMessage(content=f"I have just started the {goal} course. Please introduce yourself and start the first lesson!")],
            "module_name": first_mod,
            "goal": goal
        }
        result = socratic_agent.invoke(initial_input)
        greeting = result["messages"][-1].content
        
        return {
            welcome_screen: gr.update(visible=False),
            tutor_screen: gr.update(visible=True),
            goal_display: f"### 🎯 Goal: {goal}",
            selected_goal: goal,
            selected_mod: first_mod,
            m1: gr.update(value=f"1. {modules[0]}"),
            m2: gr.update(value=f"2. {modules[1]}"),
            m3: gr.update(value=f"3. {modules[2]}"),
            m4: gr.update(value=f"4. {modules[3]}"),
            m5: gr.update(value=f"5. {modules[4]}"),
            m6: gr.update(value=f"6. {modules[5]}"),
            chatbot_comp: [{"role": "assistant", "content": greeting}]
        }

    def set_active_module(btn_text):
        return btn_text.split(". ")[1]

    m1.click(set_active_module, m1, selected_mod, api_name=False)
    m2.click(set_active_module, m2, selected_mod, api_name=False)
    m3.click(set_active_module, m3, selected_mod, api_name=False)
    m4.click(set_active_module, m4, selected_mod, api_name=False)
    m5.click(set_active_module, m5, selected_mod, api_name=False)
    m6.click(set_active_module, m6, selected_mod, api_name=False)

    btn_cricket.click(start_course, gr.State("Cricket Game"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, m4, m5, m6, chatbot_comp], api_name=False)
    btn_blog.click(start_course, gr.State("Food Blog"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, m4, m5, m6, chatbot_comp], api_name=False)
    btn_finance.click(start_course, gr.State("Expense Tracker"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, m4, m5, m6, chatbot_comp], api_name=False)
    
    def go_back():
        return {
            welcome_screen: gr.update(visible=True),
            tutor_screen: gr.update(visible=False),
            selected_goal: None,
            chatbot_comp: []
        }

    btn_back.click(go_back, None, [welcome_screen, tutor_screen, selected_goal, chatbot_comp], api_name=False)

if __name__ == "__main__":
    demo.launch()