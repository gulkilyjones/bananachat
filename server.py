import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import cgi

# Directory to store messages
messages_directory = "messages"

# Ensure the messages directory exists
os.makedirs(messages_directory, exist_ok=True)

# Function to generate the HTML chat interface
def generate_chat_html():
    with open("chat_interface.html", "w") as html_file:
        html_file.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .chat-container {
            width: 400px;
            max-width: 90%;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .message {
            padding: 10px 20px;
            margin: 5px;
            border-radius: 15px;
            max-width: 75%;
        }
        .sender {
            background-color: #d1f7c4;
            align-self: flex-end;
        }
        .receiver {
            background-color: #f0f0f0;
            align-self: flex-start;
        }
        .chat-content {
            display: flex;
            flex-direction: column;
            padding: 10px;
            overflow-y: auto;
            height: 400px;
        }
        form {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            width: 100%;
        }
        input[type="text"] {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            width: 100%;
        }
        input[type="submit"] {
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-content">
''')

        # Add messages from files
        for filename in sorted(os.listdir(messages_directory)):
            filepath = os.path.join(messages_directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, "r") as file:
                    content = file.read().strip()
                    label = os.path.splitext(filename)[0]
                    message_class = "sender" if label.startswith(('a', 'e', 'i', 'o', 'u')) else "receiver"
                    
                    html_file.write(f'''
            <div class="message {message_class}">
                <strong>{label.capitalize()}:</strong> {content}
            </div>
''')

        # Closing HTML tags and form for new messages
        html_file.write('''
        </div>
    </div>
    <form action="/" method="post">
        <input type="text" name="message" placeholder="Write your message here..." required>
        <input type="submit" value="Send">
    </form>
</body>
</html>
''')

# Custom request handler to handle GET and POST requests
class ChatRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML file
            self.path = '/chat_interface.html'
        return super().do_GET()

    def do_POST(self):
        # Parse form data
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['Content-Length'])
            post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            message = post_data.get('message', [''])[0].strip()

            # Save message if not empty
            if message:
                # Use a simple counter for unique file names
                count = len(os.listdir(messages_directory)) + 1
                with open(os.path.join(messages_directory, f"message{count}.txt"), "w") as file:
                    file.write(message)

                # Regenerate the HTML file with the new message
                generate_chat_html()

            # Redirect back to the main page
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

# Initialize the chat HTML page
generate_chat_html()

# Run the server
server_address = ('', 8000)
httpd = HTTPServer(server_address, ChatRequestHandler)
print("Server running on http://localhost:8000")
httpd.serve_forever()

