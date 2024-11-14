# html_generator.py
import html
from datetime import datetime
from pathlib import Path
from template_manager import TemplateManager

class HtmlGenerator:
    def __init__(self):
        self.template = TemplateManager()
        self.messages_dir = Path("messages")

    def generate_html(self):
        """Generate HTML for the chat interface"""
        messages = self._get_messages()
        return self.template.render(
            title="BananaChat",
            messages=self._format_messages(messages),
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def _get_messages(self):
        """Get all messages from the messages directory"""
        messages = []
        try:
            # Get all message files
            for file in self.messages_dir.glob("*.txt"):
                try:
                    content = file.read_text().strip()
                    # Get both creation and modification times
                    stats = file.stat()
                    # Use the more recent of ctime or mtime
                    timestamp = max(stats.st_ctime, stats.st_mtime)

                    messages.append({
                        'content': content,
                        'filename': file.name,
                        'date': datetime.fromtimestamp(timestamp)
                    })
                except Exception as e:
                    print(f"Error reading {file}: {e}")

            # Sort messages by date, newest first
            messages.sort(key=lambda x: x['date'], reverse=True)

        except Exception as e:
            print(f"Error accessing messages directory: {e}")

        return messages

    def _format_messages(self, messages):
        """Format messages for display"""
        # Messages are already sorted in _get_messages()
        return [self._format_message(msg) for msg in messages]

    def _format_message(self, msg):
        return {
            'content': html.escape(msg['content']),
            'author': 'Anonymous',
            'timestamp': msg['date'].strftime('%Y-%m-%d %H:%M:%S'),
            'filename': html.escape(msg['filename']),
            'color_class': 'bg-gray-100',
            'is_system_msg': False
        }