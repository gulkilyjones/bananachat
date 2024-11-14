# server.py
import os
import http.server
import urllib.parse
from pathlib import Path
from chat_system import ChatSystem
from html_generator import HtmlGenerator
from request_handler import ChatRequestHandler
from logger import logger

def main():
    # Initialize components
    messages_dir = Path("./messages")
    messages_dir.mkdir(exist_ok=True)
    
    html_gen = HtmlGenerator()
    chat_system = ChatSystem()
    
    # Create request handler with dependencies
    handler = lambda *args: ChatRequestHandler(
        *args,
        chat_system=chat_system,
        html_generator=html_gen
    )
    
    # Start server
    server_address = ("", 8000)
    httpd = http.server.HTTPServer(server_address, handler)
    logger.info("Server running on http://localhost:8000")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        httpd.server_close()

if __name__ == "__main__":
    main()
