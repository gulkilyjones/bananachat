# message_formatter.py
import html
from datetime import datetime

class MessageFormatter:
    def format_messages(self, messages):
        """Format messages for HTML display"""
        # Sort messages by date
        sorted_msgs = sorted(messages, key=lambda x: x['date'])
        
        # Group messages by author for colored backgrounds
        authors = list(set(msg['author'] for msg in sorted_msgs))
        author_colors = self._generate_author_colors(authors)
        
        # Format each message
        formatted = []
        for msg in sorted_msgs:
            formatted.append(self._format_message(msg, author_colors))
            
        return formatted
    
    def _format_message(self, msg, author_colors):
        """Format a single message"""
        return {
            'content': html.escape(msg['content']),
            'author': html.escape(msg.get('author', 'anonymous')),
            'color_class': author_colors.get(msg['author'], 'bg-gray-100'),
            'timestamp': msg['date'].strftime('%Y-%m-%d %H:%M:%S'),
            'filename': html.escape(msg['filename']),
            'is_system_msg': msg['author'].lower() in {'system', 'admin'}
        }
    
    def _generate_author_colors(self, authors):
        """Generate consistent color classes for authors"""
        colors = [
            'bg-blue-100', 'bg-green-100', 'bg-yellow-100',
            'bg-purple-100', 'bg-pink-100', 'bg-indigo-100'
        ]
        return {
            author: colors[i % len(colors)]
            for i, author in enumerate(sorted(authors))
        }
