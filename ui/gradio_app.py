import uuid
import gradio as gr
from app.graph_builder import build_graph

graph = build_graph()

def make_thread_id() -> str:
    return str(uuid.uuid4())

async def process_message(message, success_criteria, history, thread):
    config = {"configurable": {"thread_id": thread}}
    state = {
        "messages": message,
        "success_criteria": success_criteria,
        "feedback_on_work": None,
        "success_criteria_met": False,
        "user_input_needed": False
    }
    result = await graph.ainvoke(state, config=config)
    user = {"role": "user", "content": message}
    reply = {"role": "assistant", "content": result["messages"][-2].content}
    feedback = {"role": "assistant", "content": result["messages"][-1].content}
    return history + [user, reply, feedback]

async def reset():
    return "", "", None, make_thread_id()

def launch_app():
    with gr.Blocks(theme=gr.themes.Default(primary_hue="emerald")) as demo:
        gr.Markdown("## Sidekick Personal Co-worker")
        thread = gr.State(make_thread_id())

        with gr.Row():
            chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")
        with gr.Group():
            with gr.Row():
                message = gr.Textbox(show_label=False, placeholder="Your request")
            with gr.Row():
                success_criteria = gr.Textbox(show_label=False, placeholder="What are your success criteria?")
        with gr.Row():
            reset_button = gr.Button("Reset", variant="stop")
            go_button = gr.Button("Go!", variant="primary")

        message.submit(process_message, [message, success_criteria, chatbot, thread], [chatbot])
        success_criteria.submit(process_message, [message, success_criteria, chatbot, thread], [chatbot])
        go_button.click(process_message, [message, success_criteria, chatbot, thread], [chatbot])
        reset_button.click(reset, [], [message, success_criteria, chatbot, thread])

    demo.launch()