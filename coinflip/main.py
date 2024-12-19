import asyncio
import random
from aiohttp import web

async def flip_coin():
    """Асинхронно подбрасывает монетку."""
    await asyncio.sleep(0.01)  # Уступаем управление
    return "Heads" if random.random() > 0.5 else "Tails"

async def simulate_flips(n):
    """Асинхронно подбрасывает монетку n раз."""
    tasks = [flip_coin() for _ in range(n)]
    results = await asyncio.gather(*tasks)
    counts = {"Heads": results.count("Heads"), "Tails": results.count("Tails")}
    return results, counts

async def coin_flip_handler(request):
    """Обрабатывает запросы на подбрасывание монетки."""
    try:
        n = int(request.query.get("n", "10"))
    except ValueError:
        return web.json_response({"error": "Invalid 'n' parameter"}, status=400)
    results, counts = await simulate_flips(n)
    return web.json_response({"results": results, "counts": counts})

async def init_app():
    app = web.Application()
    app.router.add_get("/coin-flip", coin_flip_handler)
    return app

if __name__ == "__main__":
    web.run_app(init_app(), port=80)
