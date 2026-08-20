import asyncio
from desktop.listeners import start_listening, stop_listening

async def main():
    loop = asyncio.get_running_loop()
    start_listening(loop)
    print("🚀 Слухачі мишки та клавіатури успішно запущені!")

    try:
        await asyncio.Event().wait()
    finally:
        stop_listening()
        print("🛑 Слухачі зупинені.")

if __name__ == "__main__":
    asyncio.run(main())