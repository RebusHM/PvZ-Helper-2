import sys
import logging

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from telegram import (
    BotCommand,
    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
    Update,
)
from telegram.request import HTTPXRequest
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN, CHECK_INTERVAL_MINUTES, PROXY_URL, API_BASE_URL
from handlers import (
    start_command,
    help_command,
    check_pvz2_command,
    check_pvz3_command,
    download_pvz2_command,
    download_pvz3_command,
    post_apk_command,
    admin_command,
    get_emoji_command,
    mods_command,
    callback_query_handler,
    any_other_message_handler,
)
from services import tracker, get_active_proxy

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("pvz_helper_bot")


async def scheduled_update_check(context: ContextTypes.DEFAULT_TYPE):
    """Background recurring task that checks Google Play and notifies channel."""
    logger.info("Running scheduled Google Play update check...")
    try:
        posted = await tracker.check_and_post_updates(context.bot)
        if posted:
            logger.info(f"Published updates to channel: {', '.join(posted)}")
        else:
            logger.info("Update check complete: No new versions.")
    except Exception as e:
        logger.error(f"Error in scheduled check: {e}", exc_info=True)


async def post_init(application):
    """Set up Telegram bot commands menu for all scopes."""
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Показать список команд"),
        BotCommand("mods", "Популярные моды на PvZ 2"),
        BotCommand("checkpvz2", "Проверить обновление PvZ2"),
        BotCommand("checkpvz3", "Проверить обновление PvZ3"),
        BotCommand("downloadpvz2", "Выгрузить APK Plants vs. Zombies 2"),
        BotCommand("downloadpvz3", "Выгрузить APK Plants vs. Zombies 3"),
        BotCommand("postapk", "Опубликовать APK в канал @NewsForPvZ"),
        BotCommand("admin", "Панель администратора"),
        BotCommand("getemoji", "Узнать ID премиум-эмодзи"),
    ]
    for scope in [BotCommandScopeDefault(), BotCommandScopeAllPrivateChats(), BotCommandScopeAllGroupChats()]:
        try:
            await application.bot.set_my_commands(commands, scope=scope)
        except Exception as e:
            logger.warning(f"Failed to set commands for scope {scope}: {e}")
    logger.info("Bot commands menu registered successfully across all scopes.")


def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "=" * 60)
        print("⚠️  ВНИМАНИЕ: BOT_TOKEN не указан в файле .env!")
        print("Пожалуйста, создайте бота у @BotFather в Telegram,")
        print("скопируйте токен в файл .env (BOT_TOKEN=...) и запустите снова.")
        print("=" * 60 + "\n")
        sys.exit(1)

    logger.info("Starting PvZ Helper Bot...")

    # Determine working proxy for bypassing network restrictions
    active_proxy = get_active_proxy(PROXY_URL)
    if active_proxy:
        logger.info(f"Bypassing network blocks via proxy: {active_proxy}")
    else:
        logger.info("Using direct network connection (no proxy).")

    # Extended timeout configuration for reliable downloading & uploading large game APKs
    request_config = HTTPXRequest(
        proxy=active_proxy,
        read_timeout=300.0,
        write_timeout=300.0,
        connect_timeout=60.0,
        pool_timeout=60.0,
    )

    # Check for Local Telegram Bot API Server (tdlib/telegram-bot-api)
    from services.local_bot_api import local_bot_api
    from config import USE_LOCAL_BOT_API, TELEGRAM_API_ID, TELEGRAM_API_HASH, LOCAL_BOT_API_PORT

    using_local_api = False
    if USE_LOCAL_BOT_API or (TELEGRAM_API_ID and TELEGRAM_API_HASH) or local_bot_api.is_port_listening():
        if local_bot_api.ensure_server_running():
            logger.info(f"🚀 Active Local Telegram Bot API server on port {LOCAL_BOT_API_PORT}! 2000MB upload limit enabled.")
            # Local Bot API does not need HTTP proxy because the local server communicates directly
            local_request = HTTPXRequest(
                read_timeout=600.0,
                write_timeout=600.0,
                connect_timeout=60.0,
                pool_timeout=60.0,
            )
            app_builder = (
                ApplicationBuilder()
                .token(BOT_TOKEN)
                .request(local_request)
                .get_updates_request(local_request)
                .base_url(local_bot_api.get_base_url())
                .base_file_url(local_bot_api.get_base_file_url())
                .local_mode(True)
                .concurrent_updates(True)
                .post_init(post_init)
            )
            using_local_api = True

    if not using_local_api:
        app_builder = (
            ApplicationBuilder()
            .token(BOT_TOKEN)
            .request(request_config)
            .get_updates_request(request_config)
            .concurrent_updates(True)
            .post_init(post_init)
        )
        if API_BASE_URL:
            logger.info(f"Using custom API base URL: {API_BASE_URL}")
            app_builder = app_builder.base_url(API_BASE_URL)

    application = app_builder.build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mods", mods_command))
    application.add_handler(CommandHandler("pvz2mods", mods_command))
    application.add_handler(CommandHandler("checkpvz2", check_pvz2_command))
    application.add_handler(CommandHandler("checkpvz3", check_pvz3_command))
    application.add_handler(CommandHandler("downloadpvz2", download_pvz2_command))
    application.add_handler(CommandHandler("downloadpvz3", download_pvz3_command))
    application.add_handler(CommandHandler("postapk", post_apk_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("getemoji", get_emoji_command))

    # Callback Queries for Inline Buttons
    application.add_handler(CallbackQueryHandler(callback_query_handler))

    # Catch-all Handler for non-command messages outside allowed chats
    application.add_handler(MessageHandler(filters.ALL, any_other_message_handler))

    # Background JobQueue for automatic Google Play polling
    job_queue = application.job_queue
    if job_queue:
        interval_seconds = max(CHECK_INTERVAL_MINUTES * 60, 60)
        job_queue.run_repeating(
            scheduled_update_check,
            interval=interval_seconds,
            first=10,
            name="google_play_update_checker",
        )
        logger.info(f"Scheduled update checker every {CHECK_INTERVAL_MINUTES} minutes.")

    # Start Polling with drop_pending_updates=False:
    # All commands sent while offline are preserved and processed immediately upon launch!
    logger.info("PvZ Helper Bot is running with drop_pending_updates=False! Press Ctrl+C to stop.")
    application.run_polling(
        drop_pending_updates=False,
        allowed_updates=Update.ALL_TYPES,
        bootstrap_retries=10,
    )


if __name__ == "__main__":
    main()
