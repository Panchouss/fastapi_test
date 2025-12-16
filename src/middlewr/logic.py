import time

async def http_performance_middleware(request, call_next):
    ip_address = request.client.host
    print(f"{ip_address=}")
    start = time.perf_counter()
    response = await call_next(request)
    end = time.perf_counter() - start
    print(f"Время обработки запроса: {end:.4f} сек.")
    return response

