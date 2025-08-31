
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import gradio as gr
from app_gradio import create_astrogeo_interface

app = FastAPI()

gradio_app = create_astrogeo_interface()

# Tell Gradio where it’s mounted
app = gr.mount_gradio_app(
    app,
    gradio_app,
    path="/astrogeo",
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/astrogeo/")
