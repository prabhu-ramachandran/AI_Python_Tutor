import gradio as gr
from fastapi import FastAPI, Request as FastRequest
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
import uvicorn
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

from logic import socratic_agent
from langchain_core.messages import HumanMessage, AIMessage
from vision import get_vision_tab, calculate_xp, get_xp_html
# Database imports
from database import save_progress, ensure_user_exists, get_user_progress
from sandbox import execute_code_safely

# --- FASTAPI & OAUTH SETUP ---
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("OAUTH_CLIENT_SECRET", "bangalore-secret-key-123"))

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.environ.get('OAUTH_CLIENT_ID'),
    client_secret=os.environ.get('OAUTH_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}
)

@app.get('/login')
async def login(request: FastRequest):
    redirect_uri = request.url_for('auth')
    redirect_uri_str = str(redirect_uri)
    if "http://" in redirect_uri_str and not "localhost" in redirect_uri_str:
        redirect_uri_str = redirect_uri_str.replace("http://", "https://")
    return await oauth.google.authorize_redirect(request, redirect_uri_str)

@app.get('/auth')
async def auth(request: FastRequest):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        if user:
            request.session['user'] = user.get('email')
        return RedirectResponse(url='/')
    except Exception as e:
        print(f"Auth Error: {e}")
        return RedirectResponse(url='/?error=auth_failed')

@app.get('/logout')
async def logout(request: FastRequest):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

# --- GRADIO APP ---

CURRICULUM = {
    "Cricket Game": ["The Stadium (I/O)", "The Scoreboard (Variables)", "The Umpire (Conditionals)", "The Over (Loops)", "The Commentary (Functions)", "Match Recap (Git)"],
    "Food Blog": ["The Menu (Strings)", "The Foodies List (Lists)", "Hotel Cards (Dictionaries)", "The Generator (Loops)", "Go Live (File I/O)", "Cloud Launch (Infra)"],
    "Expense Tracker": ["The Wallet (Data Types)", "Daily Ledger (CSV)", "App Menu (Flow)", "The Auditor (Logic)", "The Workshop (Infra)", "Portfolio (Final)"]
}

with gr.Blocks(title="Bengaluru AI Tutor", theme=gr.themes.Soft()) as demo:
    with gr.Row():
        gr.Markdown("# 🏫 Bengaluru AI Code Lab")
        with gr.Column(scale=0):
            btn_logout = gr.Button("🚪 Logout", size="sm", visible=False)

    selected_goal = gr.State(None)
    selected_mod = gr.State("Intro")

    with gr.Column(visible=False) as main_container:
        with gr.Tabs():
            with gr.TabItem("🎓 Classroom"):
                with gr.Column(visible=True) as welcome_screen:
                    gr.Markdown("## 👋 Namaskara! What do you want to build first?")
                    status_display = gr.Markdown("### 🏆 Your Level 1 Progress\n- ⚪ Cricket: 0/6\n- ⚪ Blog: 0/6\n- ⚪ Tracker: 0/6")
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 🏏 Gully Cricket Game")
                            btn_cricket = gr.Button("Choose Cricket 🏏", variant="primary")
                            gr.Video(value="static/demos/cricket_demo.mp4", label="Demo", interactive=False, autoplay=True, loop=True, show_label=False)
                        
                        with gr.Column():
                            gr.Markdown("### 🌐 Food Blog Generator")
                            btn_blog = gr.Button("Choose Food Blog 🌐", variant="primary")
                            gr.Video(value="static/demos/blog_demo.mp4", label="Demo", interactive=False, autoplay=True, loop=True, show_label=False)
                        
                        with gr.Column():
                            gr.Markdown("### 💰 Kharcha Tracker")
                            btn_finance = gr.Button("Choose Expense Tracker 💰", variant="primary")
                            gr.Video(value="static/demos/tracker_demo.mp4", label="Demo", interactive=False, autoplay=True, loop=True, show_label=False)

                with gr.Column(visible=False) as tutor_screen:
                    with gr.Row():
                        btn_back = gr.Button("⬅️ Back to Goals", size="sm")
                        goal_display = gr.Markdown("Current Goal: ...")
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### 🗺️ Your Path")
                            m1 = gr.Button("1. Module"); m2 = gr.Button("2. Module"); m3 = gr.Button("3. Module")
                            m4 = gr.Button("4. Module"); m5 = gr.Button("5. Module"); m6 = gr.Button("6. Module")
                            gr.Markdown("### 🔒 Level 2 (Locked)")
                            gr.Button("7. Advanced Engineering", interactive=False)
                            
                            gr.Markdown("---")
                            gr.Markdown("### 🕵️ Tutor's Secret Tool")
                            gr.Markdown("Real developers don't memorize everything! Stuck? **Ask me for keywords** to search on Google. Finding solutions is a superpower! 🚀")
                        
                        with gr.Column(scale=3):
                            chatbot_comp = gr.Chatbot(label="Socratic Tutor")
                            with gr.Row():
                                txt_input = gr.Textbox(show_label=False, placeholder="Type your answer here...", scale=4)
                                btn_submit = gr.Button("Send ➤", scale=1)
                            gr.Markdown("### 🐍 Python Sandbox")
                            code_input = gr.Code(language="python", label="Write your code here", lines=5)
                            btn_run = gr.Button("▶️ Run Code", variant="secondary")
                            code_output = gr.Textbox(label="Terminal Output", interactive=False, max_lines=10)
            
            logic_bar, ui_bar, db_bar = get_vision_tab()

    with gr.Column(visible=True) as login_prompt:
        gr.Markdown("### Please sign in to start your learning journey! 🚀")
        btn_login_trigger = gr.Button("Sign in with Google 🛡️", variant="primary")

    def get_status_markdown(username):
        progress = get_user_progress(username)
        completed = progress.get("completed", {}) if progress else {}
        status_msg = "### 🏆 Your Level 1 Progress\n"
        all_done = True
        for goal, modules in CURRICULUM.items():
            done_count = sum(1 for m in modules if m in completed)
            emoji = "✅" if done_count == 6 else "🟡" if done_count > 0 else "⚪"
            status_msg += f"- {emoji} **{goal}**: {done_count}/6 Modules\n"
            if done_count < 6: all_done = False
        status_msg += "\n🌟 **Level 2 Unlocked!**" if all_done else "\n*Complete all 3 projects to unlock Level 2.*"
        return status_msg

    def check_user(request: gr.Request):
        session = request.request.session
        user = session.get("user")
        
        # Local Development Bypass
        host = request.request.client.host if request.request.client else ""
        if not user and (host == "127.0.0.1" or host == "localhost" or not os.environ.get("OAUTH_CLIENT_ID")):
            user = "local-dev"
            
        if user:
            try: ensure_user_exists(user)
            except: pass
            xp = calculate_xp(user)
            return (gr.update(visible=True), gr.update(visible=False), gr.update(visible=True), 
                    get_status_markdown(user), 
                    get_xp_html("Logic", xp["Logic"], "#4a148c"), 
                    get_xp_html("Frontend", xp["Frontend"], "#1b5e20"), 
                    get_xp_html("Database", xp["Database"], "#e65100"))
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(), gr.update(), gr.update(), gr.update()

    demo.load(check_user, None, [main_container, login_prompt, btn_logout, status_display, logic_bar, ui_bar, db_bar], api_name=False)

    def submit_message(user_text, history, module_name, goal_name, request: gr.Request):
        if not user_text.strip(): return {txt_input: gr.update()}
        user = request.request.session.get("user", "guest")
        new_history = history + [{"role": "user", "content": user_text}]
        formatted_history = [HumanMessage(content=m['content']) if m['role']=='user' else AIMessage(content=m['content']) for m in new_history]
        result = socratic_agent.invoke({"messages": formatted_history, "module_name": module_name, "goal": goal_name})
        ai_response = result["messages"][-1].content
        updated_mod_state = module_name
        if "[MODULE_COMPLETE]" in ai_response:
            ai_response = ai_response.replace("[MODULE_COMPLETE]", "").strip() + "\n\n🎉 **Module Complete!**"
            modules = CURRICULUM[goal_name]
            try:
                idx = modules.index(module_name)
                if idx < 5: 
                    updated_mod_state = modules[idx+1]
                    if user != "guest": save_progress(user, goal_name, updated_mod_state, {"completed_module_name": module_name, "steps": len(new_history)//2})
            except: pass
        return {chatbot_comp: new_history + [{"role": "assistant", "content": ai_response}], txt_input: "", selected_mod: updated_mod_state}

    def run_code_and_chat(code, history, module_name, goal_name, request: gr.Request):
        output = execute_code_safely(code)
        res = submit_message(f"I ran this code:\n```python\n{code}\n```\nOutput:\n```\n{output}\n```", history, module_name, goal_name, request)
        res[code_output] = output
        return res

    txt_input.submit(submit_message, [txt_input, chatbot_comp, selected_mod, selected_goal], [chatbot_comp, txt_input, selected_mod], api_name=False)
    btn_submit.click(submit_message, [txt_input, chatbot_comp, selected_mod, selected_goal], [chatbot_comp, txt_input, selected_mod], api_name=False)
    btn_run.click(run_code_and_chat, [code_input, chatbot_comp, selected_mod, selected_goal], [chatbot_comp, txt_input, selected_mod, code_output], api_name=False)

    def start_course(goal, request: gr.Request):
        user = request.request.session.get("user", "guest")
        modules = CURRICULUM[goal]
        saved = get_user_progress(user) if user != "guest" else None
        active_mod = saved.get("module") if (saved and saved.get("goal") == goal) else modules[0]
        result = socratic_agent.invoke({"messages": [HumanMessage(content=f"Starting {goal}, module {active_mod}")], "module_name": active_mod, "goal": goal})
        return {welcome_screen: gr.update(visible=False), tutor_screen: gr.update(visible=True), goal_display: f"### 🎯 Goal: {goal}", selected_goal: goal, selected_mod: active_mod, 
                m1: gr.update(value=f"1. {modules[0]}"), m2: gr.update(value=f"2. {modules[1]}"), m3: gr.update(value=f"3. {modules[2]}"), 
                m4: gr.update(value=f"4. {modules[3]}"), m5: gr.update(value=f"5. {modules[4]}"), m6: gr.update(value=f"6. {modules[5]}"), 
                chatbot_comp: [{"role": "assistant", "content": result["messages"][-1].content}]}

    btn_cricket.click(start_course, gr.State("Cricket Game"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, m4, m5, m6, chatbot_comp], api_name=False)
    btn_blog.click(start_course, gr.State("Food Blog"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, m4, m5, m6, chatbot_comp], api_name=False)
    btn_finance.click(start_course, gr.State("Expense Tracker"), [welcome_screen, tutor_screen, goal_display, selected_goal, selected_mod, m1, m2, m3, m4, m5, m6, chatbot_comp], api_name=False)
    
    btn_back.click(lambda request: {welcome_screen: gr.update(visible=True), tutor_screen: gr.update(visible=False), selected_goal: None, chatbot_comp: [], 
                                    status_display: get_status_markdown(request.request.session.get("user", "guest"))}, 
                   None, [welcome_screen, tutor_screen, selected_goal, chatbot_comp, status_display], api_name=False)

    btn_login_trigger.click(None, None, None, js="() => { window.location.href = '/login'; }")
    btn_logout.click(None, None, None, js="() => { window.location.href = '/logout'; }")

app = gr.mount_gradio_app(app, demo, path="/")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))