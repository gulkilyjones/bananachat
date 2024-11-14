# request_handler.py
import http.server
import urllib.parse
import time
from pathlib import Path
from logger import logger

class ChatRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, chat_system=None, html_generator=None):
        self.chat_system = chat_system
        self.html_generator = html_generator
        super().__init__(*args)

    def do_GET(self):
        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Generate fresh HTML
                html_content = self.html_generator.generate_html()
                self.wfile.write(html_content.encode())
            else:
                self.send_error(404, "File Not Found")
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self.send_error(500, "Internal Server Error")

    def do_POST(self):
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode("utf-8"))
            
            message = post_data.get("message", [""])[0]
            
            if message:
                filename = f"msg_{int(time.time())}.txt"
                Path("messages").mkdir(exist_ok=True)
                (Path("messages") / filename).write_text(message)
                
            # Redirect back to chat interface
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self.send_error(500, "Internal Server Error")
