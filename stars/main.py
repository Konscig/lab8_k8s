import asyncio
import random
from aiohttp import web, ClientSession

async def generate_star_map(stars, size):
    """Асинхронно создает звездную карту."""
    await asyncio.sleep(0.01)  # Уступаем управление
    grid = [[" " for _ in range(size)] for _ in range(size)]
    for _ in range(stars):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        grid[x][y] = "*"
    return "\n".join("".join(row) for row in grid)

async def fetch_fibonacci_number(n):
    """Запрашивает n-е число Фибоначчи у соответствующего сервиса."""
    url = "http://fibonacci-service:80/fibonacci"
    async with ClientSession() as session:
        async with session.get(url, params={"n": n}) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("fibonacci", 0)
            return 0

async def star_map_handler(request):
    """Обрабатывает запросы на создание звездной карты."""
    try:
        n = int(request.query.get("n", "5"))
        size = int(request.query.get("size", "10"))
    except ValueError:
        return web.json_response({"error": "Invalid parameters"}, status=400)
    
    # Получаем n-е число Фибоначчи
    fibonacci_number = await fetch_fibonacci_number(n)
    if fibonacci_number > size * size:
        return web.json_response({"error": "Too many stars for the grid size"}, status=400)
    
    star_map = await generate_star_map(fibonacci_number, size)
    return web.Response(text=star_map, content_type="text/plain")

async def init_app():
    app = web.Application()
    app.router.add_get("/star-map", star_map_handler)
    return app

if __name__ == "__main__":
    web.run_app(init_app(), port=80)
