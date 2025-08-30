# app_gradio.py
import gradio as gr
# import your helper functions: asr, smart_bot, image_gen (define them or stub for now)

def create_astrogeo_interface():
    with gr.Blocks(title="🛰️ ASTROGEO AI Pro - Free Edition") as iface:
        gr.Markdown("# 🛰️ ASTROGEO AI Pro - Free Edition\nMulti-Modal System")

        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="🛰️ ASTROGEO AI", height=500, type="messages")
                msg = gr.Textbox(label="Text Input")
                send_btn = gr.Button("🚀 Send")

            with gr.Column(scale=1):
                gen_img = gr.Image(label="🖼️ Generated Image")
                status = gr.Textbox(label="📊 Status")

        # simple dummy processor (replace with your process_all)
        def process_all(msg_text, chat_hist):
            response = f"Echo: {msg_text}"
            chat_hist = chat_hist + [(msg_text, response)]
            return chat_hist, ""

        send_btn.click(process_all, inputs=[msg, chatbot], outputs=[chatbot, msg])

    return iface
