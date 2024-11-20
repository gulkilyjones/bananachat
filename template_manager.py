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
	<link rel="stylesheet" href="style.css">
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
