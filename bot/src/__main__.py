"""Bot main entry point."""

import logging
import sys
from pathlib import Path

from telegram.ext import Application, CommandHandler

# Add src to path for imports
SRC_PATH = Path(__file__).resolve().parent
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from config.settings import settings
from handlers.add_handler import handle_add
from handlers.start_handler import handle_start

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """Start the Telegram bot."""
    logger.info("Starting AI Content Organizer Bot...")
    logger.info(f"Backend URL: {settings.backend_url}")

    # Create the Application
    application = Application.builder().token(settings.telegram_bot_token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("add", handle_add))

    logger.info("Bot handlers registered")
    logger.info("Bot is now running. Press Ctrl+C to stop.")

    # Start the bot
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
