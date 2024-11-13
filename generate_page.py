import os

# Set the directory containing the message files
directory = "messages"

# Create an HTML file to display the chat interface
with open("chat_interface.html", "w") as html_file:
    # Write basic HTML and CSS for the chat interface
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
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
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
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-content">
''')

    # Read each file and add its content as a message in the chat
    for filename in sorted(os.listdir(directory)):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                content = file.read().strip()
                label = os.path.splitext(filename)[0]
                message_class = "sender" if label.startswith(('a', 'e', 'i', 'o', 'u')) else "receiver"
                
                # Write each message in HTML
                html_file.write(f'''
            <div class="message {message_class}">
                <strong>{label.capitalize()}:</strong> {content}
            </div>
''')

    # Close the HTML tags
    html_file.write('''
        </div>
    </div>
</body>
</html>
''')

print("Chat interface generated as 'chat_interface.html'")

