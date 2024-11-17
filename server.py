import os
import http.server
import argparse
from pathlib import Path
from chat_system import ChatSystem
from html_generator import HtmlGenerator
from request_handler import ChatRequestHandler
from logger import logger

def main():
    # Argument parsing for port
    parser = argparse.ArgumentParser(description="Start the chat server.")
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to run the server on (default: 8000)"
    )
    args = parser.parse_args()

    # Validate port range
    if not (1 <= args.port <= 65535):
        logger.error(f"Invalid port number {args.port}. Please provide a port between 1 and 65535.")
        return

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
    server_address = ("", args.port)
    httpd = http.server.HTTPServer(server_address, handler)
    logger.info(f"Server running on http://localhost:{args.port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        httpd.server_close()

if __name__ == "__main__":
    main()

