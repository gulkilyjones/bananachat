class TemplateManager:
    def render(self, title, messages, last_updated):
        """Render the HTML template with provided data"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta http-equiv="refresh" content="60">
    <style>
        body {{
            background-color: #f9fafb;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 16px;
        }}
        header {{
            margin-bottom: 24px;
        }}
        header h1 {{
            font-size: 24px;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 8px;
        }}
        header p {{
            font-size: 12px;
            color: #6b7280;
        }}
        form {{
            margin-bottom: 32px;
            position: sticky;
            top: 0;
            background-color: #f9fafb;
            padding: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}
        form .input-group {{
            display: flex;
            gap: 8px;
        }}
        input[type="text"] {{
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            font-size: 14px;
        }}
        button {{
            background-color: #3b82f6;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }}
        button:hover {{
            background-color: #2563eb;
        }}
        .message {{
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin-bottom: 16px;
        }}
        .message .header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }}
        .message .author {{
            font-weight: bold;
            color: #1f2937;
        }}
        .message .timestamp {{
            font-size: 12px;
            color: #6b7280;
        }}
        .message .content {{
            white-space: pre-wrap;
            color: #374151;
        }}
        .message .filename {{
            margin-top: 8px;
            font-size: 12px;
            color: #6b7280;
        }}
        footer {{
            margin-top: 32px;
            padding-top: 16px;
            border-top: 1px solid #e5e7eb;
            font-size: 12px;
            color: #6b7280;
        }}
        footer a {{
            color: #3b82f6;
            text-decoration: none;
        }}
        footer a:hover {{
            color: #2563eb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p>Last updated: {last_updated}</p>
        </header>
        
        <form method="POST" action="/">
            <div class="input-group">
                <input type="text" name="message"
                    placeholder="Write a message..."
                    required
                    autofocus>
                <button type="submit">Send</button>
            </div>
        </form>

        <main>
            {self._render_messages(messages)}
        </main>

        <footer>
            <p>To participate, visit the <a href="https://github.com/gulkily/bananachat">GitHub repository</a></p>
        </footer>
    </div>
</body>
</html>"""

    def _render_messages(self, messages):
        """Render the message list"""
        return '\n'.join(self._render_message(msg) for msg in messages)

    def _render_message(self, msg):
        """Render a single message"""
        return f"""
        <div class="message" style="background-color: {msg['color_class']};">
            <div class="header">
                <div class="author">{msg['author']}</div>
                <div class="timestamp">{msg['timestamp']}</div>
            </div>
            <div class="content">{msg['content']}</div>
            <div class="filename">File: {msg['filename']}</div>
        </div>"""
