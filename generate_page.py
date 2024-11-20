import os

# Define the path to the directory containing message files
messages_dir = "messages"

# Set to store unique file paths
unique_message_files = set()

# Traverse the messages directory, including subdirectories
for root, _, files in os.walk(messages_dir):
    for file in files:
        if file.endswith(".txt"):  # Only include .txt files
            file_path = os.path.join(root, file)
            unique_message_files.add(file_path)  # Automatically ignore duplicates

# Convert set to a sorted list
sorted_message_files = sorted(unique_message_files)

# Create HTML structure
html_content = """
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
            background-color: #f7f7f7; 
        }
        .chat-container { 
            max-width: 600px; 
            width: 100%; 
            background-color: #fff; 
            border-radius: 8px; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            overflow: hidden; 
        }
        .chat-content { 
            display: flex; 
            flex-direction: column; 
            padding: 20px; 
            overflow-y: auto; 
            max-height: 400px; 
        }
        .message { 
            padding: 10px 15px; 
            margin: 5px 0; 
            border-radius: 15px; 
            max-width: 70%; 
        }
        .sent { 
            background-color: #DCF8C6; 
            align-self: flex-end; 
        }
        .received { 
            background-color: #E0E0E0; 
            align-self: flex-start; 
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-content">
"""

# Loop through the unique sorted files and add each to the HTML
for index, filepath in enumerate(sorted_message_files):
    # Read the content of each text file
    with open(filepath, "r") as file:
        content = file.read().strip()
    
    # Determine if the message is 'sent' or 'received' based on index
    message_class = "sent" if index % 2 == 0 else "received"

    # Append the message content to the HTML structure
    label = os.path.splitext(os.path.basename(filepath))[0]
    html_content += f'<div class="message {message_class}"><strong>{label.capitalize()}:</strong> {content}</div>\n'

# Close the HTML structure
html_content += """
        </div>
    </div>
</body>
</html>
"""

# Save to an HTML file
with open("chat_interface.html", "w") as html_file:
    html_file.write(html_content)

print("HTML chat interface generated as 'chat_interface.html'.")
