
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve frontend files from 'static'
app.mount("/astrogeo", StaticFiles(directory="static", html=True), name="astrogeo")

@app.get("/")
async def root():
    # Instead of redirect loop, directly serve /astrogeo
    return RedirectResponse(url="/astrogeo/")
