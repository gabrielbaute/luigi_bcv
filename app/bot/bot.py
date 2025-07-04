from telegram.ext import Application, CommandHandler

from app.settings import Config
from app.app_log import get_logger
from app.core import Divisas
from app.bot.commands import start, dolar, euro, lira, rublo, yuan

logger = get_logger(f"[{Config().APP_NAME}]")

TOKEN = Config().TELEGRAM_BOT_KEY  

async def post_init(application: Application):
    """Función que se ejecuta después de que la aplicación se haya inicializado."""

    logger.info("🔗 Configurando el webhook del bot de Telegram...")
    await application.bot.delete_webhook(drop_pending_updates=True)

def main():    
    logger.info("🔗 Iniciando el bot de Telegram...")

    # Verifica que el token esté 
    if not TOKEN:
        logger.error("❌ No se encontró TELEGRAM_BOT_KEY en las variables de entorno")
        raise ValueError("Token de Telegram no configurado")
    else:
        logger.info("✅ Token de Telegram encontrado")

    application = Application.builder().token(TOKEN).post_init(post_init).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler(f"{Divisas.DOLAR.value}", dolar))
    application.add_handler(CommandHandler(f"{Divisas.EURO.value}", euro))
    application.add_handler(CommandHandler(f"{Divisas.LIRA.value}", lira))
    application.add_handler(CommandHandler(f"{Divisas.RUBLE.value}", rublo))
    application.add_handler(CommandHandler(f"{Divisas.YUAN.value}", yuan))
    
    try:
        application.run_polling()
        logger.info("Bot iniciado. Usa /start para ver las opciones")
    except Exception as e:
        logger.error(f"Error al iniciar el bot: {e}")
        raise e