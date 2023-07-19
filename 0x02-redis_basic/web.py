import redis
import requests
from functools import wraps

redis_store = redis.Redis()


def data_cacher(method):
    @wraps(method)
    def invoker(url):
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


# Example usage
url = 'http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com'
content = get_page(url)
print(content)

