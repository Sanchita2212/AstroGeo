# main.py
from fastapi import FastAPI
import gradio as gr
from app_gradio import create_astrogeo_interface

# Initialize FastAPI app
app = FastAPI()

# Create your Gradio interface
gradio_app = create_astrogeo_interface()

# Mount Gradio at /astrogeo
app = gr.mount_gradio_app(app, gradio_app, path="/astrogeo")

# Root endpoint
@app.get("/")
def root():
    return {
        "status": "ASTROGEO API running",
        "gradio_ui": "/astrogeo"  # <-- helpful redirect info
    }
