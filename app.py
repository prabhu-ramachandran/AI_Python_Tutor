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
        "Setup: The Stadium (Print & Input)",
        "Scoreboard: Storing Runs (Variables)",
        "Umpire: Out or Not Out? (Conditionals)"
    ],
    "Food Blog": [
        "Menu Card: Writing Text (Strings)",
        "Top Hotels: Making a List (Lists)",
        "Publishing: Saving to File (File I/O)"
    ],
    "Expense Tracker": [
        "Pocket Money: The Wallet (Integers)",
        "Bill Total: Adding it up (Math)",
        "Daily Log: Keeping Track (Loops)"
    ]
}

# UI Layout
with gr.Blocks(title="Bengaluru AI Tutor") as demo:
    gr.Markdown("# 🏫 Bengaluru AI Code Lab")
    
    # State Management
    current_view = gr.State("selection")
    selected_goal = gr.State(None)
    selected_mod = gr.State("Intro")

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
                        m1 = gr.Button("1. Basics & Setup")
                        m2 = gr.Button("2. Variables")
                        m3 = gr.Button("3. Logic & Decisions")

                        gr.Markdown("### 🔒 Level 2 (Locked)")
                        gr.Button("4. Functions & Logic", interactive=False)
                        gr.Button("5. Data Structures", interactive=False)
                        
                        gr.Markdown("### 🔒 Level 3 (Locked)")
                        gr.Button("6. Final Project", interactive=False)

                    with gr.Column(scale=3):
                        chatbot_comp = gr.Chatbot(label="Socratic Tutor")
                        with gr.Row():
                            txt_input = gr.Textbox(show_label=False, placeholder="Type your answer here...", scale=4)
                            btn_submit = gr.Button("Send ➤", scale=1)
        
        # Add the Vision Tab
        get_vision_tab()

    # --- Chat Logic with Side Effects ---
    def submit_message(user_text, history, module_name, goal_name):
        if not user_text.strip():
            return {txt_input: gr.update()} # Do nothing if empty

        # 1. Update history with user message
        new_history = history + [{"role": "user", "content": user_text}]
        
        # 2. Convert for Agent
        formatted_history = []
        for msg in new_history:
            if msg['role'] == 'user':
                formatted_history.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                formatted_history.append(AIMessage(content=msg['content']))

        # 3. Call Agent
        input_state = {
            "messages": formatted_history,
            "module_name": module_name,
            "goal": goal_name
        }
        result = socratic_agent.invoke(input_state)
        ai_response = result["messages"][-1].content
        
        # 4. Check for [MODULE_COMPLETE] signal
        next_mod_update = gr.update()
        updated_mod_state = module_name
        
        if "[MODULE_COMPLETE]" in ai_response:
            ai_response = ai_response.replace("[MODULE_COMPLETE]", "").strip()
            ai_response += "\n\n🎉 **Module Complete! Unlocking the next level...**"
            
            # Logic to switch to next module (simple hardcoded sequence for now)
            modules = CURRICULUM[goal_name]
            try:
                current_idx = -1
                for i, m in enumerate(modules):
                    if m == module_name:
                        current_idx = i
                        break
                
                if current_idx != -1 and current_idx < len(modules) - 1:
                    next_mod_name = modules[current_idx + 1]
                    updated_mod_state = next_mod_name
                    # Highlight the next button (simulation)
                    # Ideally we would update the specific button color here
            except:
                pass

        # 5. Final History Update
        final_history = new_history + [{"role": "assistant", "content": ai_response}]
        
        return {
            chatbot_comp: final_history,
            txt_input: "",  # Clear input
            selected_mod: updated_mod_state
        }

    # Wire up the Custom Chat
    txt_input.submit(
        submit_message, 
        [txt_input, chatbot_comp, selected_mod, selected_goal], 
        [chatbot_comp, txt_input, selected_mod]
    )
    btn_submit.click(
        submit_message, 
        [txt_input, chatbot_comp, selected_mod, selected_goal], 
        [chatbot_comp, txt_input, selected_mod]
    )

    # --- Logic for View Switching ---
    def start_course(goal):
        modules = CURRICULUM[goal]
        first_mod = modules[0]
        
        # Get an initial greeting from the AI
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
            chatbot_comp: [{"role": "assistant", "content": greeting}]
        }

    def set_active_module(btn_text):
        # Extract the module name (remove "1. " prefix)
        return btn_text.split(". ")[1]

    # Link module buttons to state
    m1.click(set_active_module, m1, selected_mod)
    m2.click(set_active_module, m2, selected_mod)
    m3.click(set_active_module, m3, selected_mod)

    btn_cricket.click(start_course, gr.State("Cricket Game"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, chatbot_comp])
    btn_blog.click(start_course, gr.State("Food Blog"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, chatbot_comp])
    btn_finance.click(start_course, gr.State("Expense Tracker"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, chatbot_comp])
    
    def go_back():
        return {
            welcome_screen: gr.update(visible=True),
            tutor_screen: gr.update(visible=False),
            selected_goal: None,
            chatbot_comp: []
        }

    btn_back.click(go_back, None, [welcome_screen, tutor_screen, selected_goal, chatbot_comp])

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())