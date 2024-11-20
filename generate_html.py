# generate_html.py
import os
import json
import html
from pathlib import Path
from datetime import datetime
from chat_system import ChatSystem
from message_formatter import MessageFormatter
from template_manager import TemplateManager

def main():
    # Initialize components
    chat = ChatSystem()
    formatter = MessageFormatter()
    template = TemplateManager()
    
    # Get messages from cache or fetch new ones
    chat.update_cache()
    messages = chat.cache.get_messages()
    
    # Format messages for display
    formatted_messages = formatter.format_messages(messages)
    
    # Generate HTML
    html_content = template.render(
        title="BananaChat",
        messages=formatted_messages,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Write output
    output_path = Path('index.html')
    output_path.write_text(html_content)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    main()
