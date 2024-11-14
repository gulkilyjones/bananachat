# template_manager.py
class TemplateManager:
    def render(self, title, messages, last_updated):
        """Render the HTML template with provided data"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta http-equiv="refresh" content="60">
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto p-4">
        <header class="mb-6">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">{title}</h1>
            <p class="text-sm text-gray-500">Last updated: {last_updated}</p>
        </header>
        
        <form method="POST" action="/" class="mb-8 sticky top-0 bg-gray-50 p-4 shadow-lg rounded-lg">
            <div class="flex gap-2">
                <input type="text" name="message"
                    placeholder="Write a message..."
                    class="flex-1 rounded-lg border border-gray-300 px-4 py-2"
                    required
                    autofocus>
                <button type="submit"
                    class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
                    Send
                </button>
            </div>
        </form>

        <main class="space-y-4">
            {self._render_messages(messages)}
        </main>

        <footer class="mt-8 pt-4 border-t border-gray-200 text-sm text-gray-500">
            <p>To participate, visit the <a href="https://github.com/gulkily/bananachat"
               class="text-blue-500 hover:text-blue-700">GitHub repository</a></p>
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
        <div class="p-4 rounded-lg shadow-sm {msg['color_class']}">
            <div class="flex items-start justify-between">
                <div class="font-medium text-gray-900">{msg['author']}</div>
                <div class="text-sm text-gray-500">{msg['timestamp']}</div>
            </div>
            <div class="mt-2 whitespace-pre-wrap text-gray-800">{msg['content']}</div>
            <div class="mt-2 text-xs text-gray-500">File: {msg['filename']}</div>
        </div>"""