import os

# Define the path to the directory containing message files
messages_dir = "./messages"

# Set to store unique file paths
unique_message_files = set()

# Traverse the messages directory, including subdirectories
for root, _, files in os.walk(messages_dir):
    for file in files:
        if file.endswith(".txt"):  # Only include .txt files
            file_path = os.path.join(root, file)
            unique_message_files.add(
                file_path)  # Automatically ignore duplicates

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
        body { font-family: Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 20px; }
        .chat-container { max-width: 600px; margin: auto; padding: 10px; background-color: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }
        .message { padding: 8px 15px; margin: 5px 0; border-radius: 15px; max-width: 70%; }
        .sent { background-color: #DCF8C6; align-self: flex-end; margin-left: auto; }
        .received { background-color: #E0E0E0; align-self: flex-start; }
    </style>
</head>
<body>
    <div class="chat-container">
"""

# Loop through the unique sorted files and add each to the HTML
for index, filepath in enumerate(sorted_message_files):
    # Read the content of each text file
    with open(filepath, "r") as file:
        content = file.read().strip()

    # Determine if the message is 'sent' or 'received' based on index
    message_class = "sent" if index % 2 == 0 else "received"

    # Append the message content to the HTML structure
    html_content += f'<div class="message {message_class}">{content}</div>\n'

# Close the HTML structure
html_content += """
    </div>
</body>
</html>
"""

# Save to an HTML file
with open("chat_interface.html", "w") as html_file:
    html_file.write(html_content)

print("HTML chat interface generated as 'chat_interface.html'.")
