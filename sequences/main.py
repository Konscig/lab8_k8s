import asyncio
import random
from aiohttp import web

async def generate_sequence(length, min_value, max_value):
    """Асинхронно создает случайную числовую последовательность."""
    await asyncio.sleep(0)  # Уступаем управление
    sequence = [random.randint(min_value, max_value) for _ in range(length)]
    return sequence

async def generate_sequences(length, min_value, max_value, num_sequences):
    """Асинхронно создает несколько числовых последовательностей."""
    tasks = [
        asyncio.create_task(generate_sequence(length, min_value, max_value))
        for _ in range(num_sequences)
    ]
    sequences = await asyncio.gather(*tasks)  # Собираем результаты всех задач
    return sequences

async def sequence_handler(request):
    """Обрабатывает запросы на создание числовых последовательностей."""
    try:
        length = int(request.query.get("length", "10"))
        min_value = int(request.query.get("min", "1"))
        max_value = int(request.query.get("max", "100"))
        num_sequences = int(request.query.get("num_sequences", "3"))
    except ValueError:
        return web.json_response({"error": "Invalid parameters"}, status=400)
    if length <= 0 or min_value > max_value or num_sequences <= 0:
        return web.json_response({"error": "Invalid range or parameters"}, status=400)
    sequences = await generate_sequences(length, min_value, max_value, num_sequences)
    return web.json_response({"sequences": sequences})

async def init_app():
    app = web.Application()
    app.router.add_get("/generate-sequences", sequence_handler)
    return app

if __name__ == "__main__":
    web.run_app(init_app(), port=80)
