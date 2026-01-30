import os
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
import operator
from dotenv import load_dotenv

load_dotenv()

# State definition
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    module_name: str
    goal: str

# The Socratic Teacher Logic
def call_model(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")
    
    current_goal = state.get('goal', 'General Python Learning')
    
    system_prompt = SystemMessage(content=(
        f"You are a Socratic Python Tutor for an NGO in Bangalore. "
        f"The student is working towards this goal: {current_goal}. "
        f"The current module is: {state['module_name']}. "
        "RULES: \n"
        "1. NEVER give the full code answer.\n"
        "2. Always ask one leading question at a time.\n"
        "3. Use local Bangalore analogies (cricket, silk sarees, traffic, metro) that relate to the current goal.\n"
        "4. If they get it right, celebrate and move to the next concept with a new question.\n"
        "5. IMPORTANT: When the student has clearly mastered the CURRENT concept/module, append the tag '[MODULE_COMPLETE]' to the end of your message.\n"
        "6. ENCOURAGE SELF-SUFFICIENCY: If a student is stuck on a technical error or syntax, do not just give the answer. Encourage them to search on Google. "
        "Teach them WHAT to search for (e.g., 'How to print a variable in Python'). Give them the specific 'Keywords' to use."
    ))
    
    try:
        response = llm.invoke([system_prompt] + state["messages"])
        
        # Ensure content is a string (handle potential list of content blocks)
        if isinstance(response.content, list):
            text_content = "".join([part["text"] for part in response.content if part["type"] == "text"])
            response.content = text_content
            
        return {"messages": [response]}
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ [GEMINI API ERROR]: {error_msg}\n")
        
        # MOCK DATA FOR TESTING WHEN BLOCKED
        MOCK_RESPONSES = {
            "Cricket Game": [
                "Namaskara! I am your coach. Let's build that Cricket Game! To start, how do we tell the computer to show a message like 'Welcome to Chinnaswamy' on the screen?",
                "Exactly! We use `print()`. Now, if you want to print 'Chinnaswamy', do you put it inside quotes like 'this' or just write it normally?",
                "Shabash! Quotes it is. You have mastered the print function! Now we can move to storing the score. [MODULE_COMPLETE]"
            ]
        }
        
        # Try to find a logical mock response based on history length
        goal = state.get('goal', 'Cricket Game')
        history_len = len(state['messages'])
        
        if goal in MOCK_RESPONSES:
            mock_index = min(history_len // 2, len(MOCK_RESPONSES[goal]) - 1)
            fallback_text = MOCK_RESPONSES[goal][mock_index]
        else:
            fallback_text = (
                "Oh! Our digital stadium is having a power cut (Quota Exceeded). "
                "Even the floodlights at Chinnaswamy need a break! Please try again later. ☕"
            )
            
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=fallback_text)]}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("teacher", call_model)
workflow.add_edge(START, "teacher")
workflow.add_edge("teacher", END)

# Compile the agent
socratic_agent = workflow.compile()