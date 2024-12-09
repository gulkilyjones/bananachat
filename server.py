import os
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import cgi
from pathlib import Path
import html

# Directory to store messages
messages_directory = Path("./messages")
messages_directory.mkdir(exist_ok=True)  # Ensure the messages directory exists

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
		for filename in sorted(messages_directory.iterdir()):
			if filename.is_file() and filename.suffix == '.txt':
				with filename.open("r") as file:
					content = file.read().strip()
					# Escape HTML characters in the content
					escaped_content = html.escape(content)
					label = filename.stem
					# Escape HTML characters in the label
					escaped_label = html.escape(label)
					message_class = "sender" if label.startswith(('a', 'e', 'i', 'o', 'u')) else "receiver"

					html_file.write(f'''
			<div class="message {message_class}">
				<strong>{escaped_label.capitalize()}:</strong> {escaped_content}
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
				count = len(list(messages_directory.iterdir())) + 1
				with open(messages_directory / f"message{count}.txt", "w") as file:
					# Store the raw message (unescaped) in the file
					file.write(message)

				# Regenerate the HTML file with the new message
				generate_chat_html()

			# Redirect back to the main page
			self.send_response(303)
			self.send_header('Location', '/')
			self.end_headers()

# Command-line argument parsing
def main():
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
		print(f"Error: Invalid port number {args.port}. Please provide a port between 1 and 65535.")
		return

	# Initialize the chat HTML page
	generate_chat_html()

	# Start the server
	server_address = ("", args.port)
	httpd = HTTPServer(server_address, ChatRequestHandler)
	print(f"Server running on http://localhost:{args.port}")

	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("Server shutting down...")
		httpd.server_close()

if __name__ == "__main__":
	main()