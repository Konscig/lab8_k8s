import asyncio
from aiohttp import web

async def fibonacci_worker(n, results, index):
    """Асинхронный воркер для вычисления числа Фибоначчи."""
    if n == 0:
        results[index] = 0
    elif n == 1:
        results[index] = 1
    else:
        await asyncio.sleep(0.01)  # Имитация асинхронной работы
        results[index] = results[index - 1] + results[index - 2]

async def generate_fibonacci(n):
    """Создает последовательность Фибоначчи с использованием asyncio.Task."""
    results = [0] * n
    tasks = []

    for i in range(n):
        task = asyncio.create_task(fibonacci_worker(i, results, i))
        tasks.append(task)

    # Ожидание завершения всех задач
    await asyncio.gather(*tasks)
    return results

async def fibonacci_handler(request):
    """Обработчик HTTP-запроса."""
    try:
        n = int(request.query.get("n", 10))
        if n <= 0:
            raise ValueError
        fib_sequence = await generate_fibonacci(n)
        return web.json_response({"fibonacci": fib_sequence})
    except ValueError:
        return web.json_response({"error": "Invalid number"}, status=400)

app = web.Application()
app.router.add_get("/fibonacci", fibonacci_handler)

if __name__ == "__main__":
    web.run_app(app, port=80)
