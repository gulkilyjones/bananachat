import os
import http.server
import urllib.parse
from io import BytesIO

# Define paths
messages_dir = "./messages"
html_file_path = "chat_interface.html"

# Function to update HTML file
def update_html_file():
    message_files = sorted(os.listdir(messages_dir))
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat Interface</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 20px; }
            .chat-container { max-width: 600px; margin: auto; padding: 10px; background-color: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }
            .message { padding: 8px 15px; margin: 5px 0; border-radius: 15px; max-width: 70%; }
            .sent { background-color: #DCF8C6; align-self: flex-end; margin-left: auto; }
            .received { background-color: #E0E0E0; align-self: flex-start; }
            .message-form { display: flex; margin-top: 20px; }
            .message-input { flex: 1; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
            .message-submit { padding: 10px 20px; border-radius: 5px; background-color: #4CAF50; color: white; border: none; margin-left: 10px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="chat-container">
    """

    # Append messages in chat format
    for index, filename in enumerate(message_files):
        filepath = os.path.join(messages_dir, filename)
        if os.path.isfile(filepath) and filename.endswith(".txt"):
            with open(filepath, "r") as file:
                content = file.read().strip()
            message_class = "sent" if index % 2 == 0 else "received"
            html_content += f'<div class="message {message_class}">{content}</div>\n'

    # Add form for new message submission
    html_content += """
        </div>
        <form method="POST" action="/" class="message-form">
            <input type="text" name="message" placeholder="Write a message..." class="message-input" required>
            <input type="submit" value="Send" class="message-submit">
        </form>
    </body>
    </html>
    """

    # Write the updated HTML to the file
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

# Initial call to generate HTML file
update_html_file()

# Define HTTP request handler
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML file for the root path
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(html_file_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        # Handle message submission
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        post_data = urllib.parse.parse_qs(post_data.decode("utf-8"))
        
        # Extract the message
        new_message = post_data.get("message", [""])[0]
        
        # Save the new message as a text file
        if new_message:
            message_count = len(os.listdir(messages_dir))
            new_message_file = os.path.join(messages_dir, f"text{message_count + 1}.txt")
            with open(new_message_file, "w") as file:
                file.write(new_message)
            
            # Update HTML file with the new message
            update_html_file()
        
        # Redirect back to the chat interface
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

# Run the server
if __name__ == "__main__":
    os.makedirs(messages_dir, exist_ok=True)  # Ensure the messages directory exists

    # Create the server
    server_address = ("", 8000)
    httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()

