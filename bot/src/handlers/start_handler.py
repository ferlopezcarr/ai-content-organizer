"""Start command handler."""


async def handle_start(update, context):
    """Handle /start command."""
    help_text = """
🤖 *AI Content Organizer Bot*

Available commands:
• `/add [URL]` - Add content from LinkedIn URL
• `/ask [question]` - Ask about your knowledge base
• `/search [query]` - Search your content
• `/browse` - Browse by categories
• `/history` - View chat history

Start by adding some LinkedIn posts and then ask questions about them!
"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=help_text, parse_mode="Markdown"
    )
