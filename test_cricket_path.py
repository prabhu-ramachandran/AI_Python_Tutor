from logic import socratic_agent
from langchain_core.messages import HumanMessage

def simulate_student_interaction():
    goal = "Cricket Game"
    module = "Setup: The Stadium (Print & Input)"
    
    # 1. First interaction: Student says "Hi"
    print(f"--- Goal: {goal} | Module: {module} ---")
    print("Student: Hi! I want to build the cricket game.")
    
    input_state = {
        "messages": [HumanMessage(content="Hi! I want to build the cricket game.")],
        "module_name": module,
        "goal": goal
    }
    
    result = socratic_agent.invoke(input_state)
    ai_response = result["messages"][-1].content
    print(f"Tutor: {ai_response}")
    print("\n" + "="*50 + "\n")

    # 2. Second interaction: Student asks "How do I start?"
    print("Student: How do I start?")
    input_state["messages"].append(HumanMessage(content=ai_response))
    input_state["messages"].append(HumanMessage(content="How do I start?"))
    
    result = socratic_agent.invoke(input_state)
    ai_response = result["messages"][-1].content
    print(f"Tutor: {ai_response}")

if __name__ == "__main__":
    simulate_student_interaction()
