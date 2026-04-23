# Main script for FastAPI deployment

from fastapi import FastAPI # Import framework for webbservice.
from fastapi.responses import HTMLResponse # Return HTML instead of json for visual demo in browser.
import socket # Imports responses from containers to demonstrate communication. 
import os # Reads environment variables. 

app = FastAPI() # creates the main app, everything below is connected to the main app.

@app.get("/", response_class=HTMLResponse) # Root endpoint trough HTTP GET, returns HTML
def root(): # Function that runs when / is called
    return f""" 
    <h1>FastAPI running in K3s 🚀</h1>
    <p>Hostname: {socket.gethostname()}</p> 
    <p>Environment: {os.getenv("APP_ENV", "dev")}</p>
    """

@app.get("/health") # Endpoint for /health
def health():
    return {"status": "ok"} # Returns status

@app.get("/info") # Endpoint for /info
def info():
    return {
        "app": "fastapi-k3s",
        "hostname": socket.gethostname()  # Returns names and pods
    }

# Clarifications
# FastAPI() - Creates application
# @app.get - Definies route
# / - HTML page
# /health - Status check
# /info - App info
# socket  - Shows pods
# os - Reads env vars (environment variables)

# Browser -> Service (k3s) -> pod (container) -> FastAPI app -> Response