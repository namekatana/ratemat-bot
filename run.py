import asyncio
import logging

from app.bot import create_bot, create_dispatcher
from app.services.admin_notifier import run_admin_notifier


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = create_bot()
    dispatcher = create_dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    notifier = asyncio.create_task(run_admin_notifier(bot))
    try:
        await dispatcher.start_polling(bot)
    finally:
        notifier.cancel()


if __name__ == "__main__":
    asyncio.run(main())
