"""
Main entry point for the application.
"""

from dotenv import load_dotenv
import uvicorn

from src.app import create_app


load_dotenv(".env")

app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.server:app", host="127.0.0.1", port=5000, reload=True)
