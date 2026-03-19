"""Handler for /add command - extracts content from URLs."""

import logging

import httpx
from telegram import Update
from telegram.ext import ContextTypes

from clients.backend_client import backend_client

logger = logging.getLogger(__name__)


async def handle_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /add command to extract content from a URL.

    Usage: /add <URL>

    Extracts content from the provided URL (currently supports LinkedIn)
    and displays a preview of the extracted information.

    Args:
        update: Telegram update object
        context: Bot context with user message and bot instance
    """
    # Check if URL was provided
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "⚠️ Please provide a URL.\n\n"
            "Usage: `/add <URL>`\n\n"
            "Example: `/add https://www.linkedin.com/posts/user_post123`",
            parse_mode="Markdown",
        )
        return

    url = context.args[0]

    # Send "processing" message
    processing_msg = await update.message.reply_text(
        "🔍 Extracting content from URL...", parse_mode="Markdown"
    )

    try:
        # Call backend to extract content
        result = await backend_client.extract_content(url)

        # Format the response
        title = result.get("title", "No title")
        author = result.get("author", "Unknown author")
        text = result.get("text", "")
        metadata = result.get("metadata", {})

        # Create preview text (first 300 characters)
        preview = text[:300] + "..." if len(text) > 300 else text

        # Build response message
        response = "✅ *Content Extracted Successfully*\n\n"
        response += f"📝 *Title:* {title}\n"
        response += f"👤 *Author:* {author}\n\n"
        response += f"*Preview:*\n{preview}\n\n"

        if metadata:
            response += f"📊 *Metadata:* {len(metadata)} fields\n\n"

        response += "💾 Content saved to your knowledge base!\n\n"
        response += "_You can search this content with /search or ask questions with /ask_"

        # Delete processing message and send result
        await processing_msg.delete()
        await update.message.reply_text(response, parse_mode="Markdown")

        logger.info(f"Successfully extracted content from {url}")

    except httpx.HTTPStatusError as e:
        error_msg = "❌ *Failed to extract content*\n\n"

        if e.response.status_code == 400:
            detail = e.response.json().get("detail", "Unknown error")
            if "unsupported" in detail.lower():
                error_msg += (
                    "This URL is not supported. Currently only LinkedIn URLs are supported.\n\n"
                )
                error_msg += "Example: `https://www.linkedin.com/posts/user_post123`"
            else:
                error_msg += f"Error: {detail}"
        elif e.response.status_code == 500:
            error_msg += "The backend service encountered an error. Please try again later."
        else:
            error_msg += f"HTTP error {e.response.status_code}: {str(e)}"

        await processing_msg.delete()
        await update.message.reply_text(error_msg, parse_mode="Markdown")
        logger.error(f"HTTP error extracting content from {url}: {e}")

    except httpx.RequestError as e:
        error_msg = "❌ *Network Error*\n\n"
        error_msg += "Could not connect to the backend service. Please try again later."

        await processing_msg.delete()
        await update.message.reply_text(error_msg, parse_mode="Markdown")
        logger.error(f"Network error extracting content from {url}: {e}")

    except Exception as e:
        error_msg = "❌ *Unexpected Error*\n\n"
        error_msg += "Something went wrong. Please try again later."

        await processing_msg.delete()
        await update.message.reply_text(error_msg, parse_mode="Markdown")
        logger.exception(f"Unexpected error extracting content from {url}: {e}")
