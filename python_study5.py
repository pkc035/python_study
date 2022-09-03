# 220903

# 프로세스 기반 비동기 실행
# 다중 프로세스는 I/O 바운드한 처리뿐만 아니라 숫잣값 계산 등.. CPU 바운드한 처리의 고속화에도 유효함.
# 여러 코어를 동시에 사용해 병렬 처리를 수행할 수 있기 때문

import os, sys, time
from concurrent.futures import( ThreadPoolExecutor,ProcessPoolExecutor, as_completed)

def elapsed_time(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        v = f(*args, **kwargs)
        print(f"{f.__name__}: {time.time() - start}")
        return v
    return wrapper

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, b + a
    else:
        return a

@elapsed_time
def get_sequentail(nums):
    for num in nums:
        print(fibonacci(num))

# 순차 처리로 실행할 경우 100초 정도 걸림
# 순차 처리에 비해 다중 프로세스 처리는 22초 정도 걸림
# 다중 쓰레드로 샐행할 경우 100초 정도로 순차 처리와 비슷하게 나옴
# 최적의 병렬 숫자는 쓰레드, 프로세스 모두에서 다양한 요서의 조합에 따라 결정 됨.

@elapsed_time
def get_multi_process(nums):
    with ProcessPoolExecutor() as e:
        futures = [e.submit(fibonacci, num) for num in nums]
    
    for future in as_completed(futures):
        print(future.result())

@elapsed_time
def get_multi_thread(nums):
    with ThreadPoolExecutor() as e:
        futures = [e.submit(fibonacci, num) for num in nums]
    
    for future in as_completed(futures):
        print(future.result())

def main():
    # n = int(sys.argv[1])
    n = [1000000] * os.cpu_count()
    # print(get_sequentail(n))
    # get_multi_process(n)
    get_multi_thread(n)


# asyncio 모듈(이벤트 루프를 사용한 동시 처리 수행)
# 단일 쓰레드에서도 동시 처리가 가능하여 성능 면에서 효율성이 높아짐.

# 코루틴(서브 루틴과 같이 일련의 처리를 모아둔 것)
# 서브 루틴은 함수에 해당하고, 한번 호출되면 앞에서부터 마지막까지 한번에 실행
# 이 특성을 이용하면 여러 처리가 동시에 이루어지도록 구현할 수 있음.

import asyncio
import random
# 아직 중단하는 포인트가 없으므로 본질적으로 코루틴으로 부를 수 없고 경고 표시는 이점을 지적하는 문장

# await문 처리를 중단시키는 포인트는 I/O 처리에 의한 대기 시간이 발생하는 위치와 그 처리를 호출하는 위치


async def coro():
    return 1

# asyncio.sleep으로 처리를 중단한 이유는 I/O 처리에 따른 대기 시간이 발생하기 때문
async def call_web_api(url):
    print(f'send a request: {url}')
    await asyncio.sleep(random.random())
    print(f'got a response: {url}')
    return url

async def async_download(url):
    response = await call_web_api(url)
    return response

# 여러 코루틴을 받아 각각의 실행을 스케줄리앟함. gather 함수에 전달된 순서대로 동시에 수신되지만,
# 응답은 먼저 반환된 것부터 순서대로 처리됨, result 값은 응답 처리 순서와 관계없이 gather에 전달된 순서가 유지 됨.

async def main():
    task = asyncio.gather(async_download('https://twitter.com/'),
    async_download('https://facebook.com'),
    async_download('https://instagram.com'),)

    return await task


# 코루틴을 동작하기 위해서는 이벤트 루프와 태스크가 필요함, 코루틴은 실행이 스케줄링되면 태스크가 됨
# 이벤트 루프가 I/O 이벤트에 맞춰 태스크 실행을 제어
# 한개의 이벤트 루프는 동시에 한 개의 태스크 밖에 실행할 수 없지만, 실행 중 태스크가 중단되었을 경우
# 실행 가능한 다른 태스크를 샐행할 수 있다.

# asynio.run 함수를 호출하면 새로운 이벤트 루프가 만들어지고, 이벤트 루프가 코루틴 실행을 제어
# 현재 실행중인 이벤트 루프를 asyncio.get_running_loop 함수로 얻을 수 있음.

async def main2():
    loop = asyncio.get_running_loop()
    print(loop)

# 코루틴을 세가지 방법으로 실행할 수 있음
# 1. asyncio.run 함수에 전달, 2. 코루틴 내부에서 await 코루틴을 실행, 3. 태스크

async def coro2(n):
    await asyncio.sleep(n)
    return n

async def main3():
    task1 = asyncio.create_task(coro2(1))
    task2 = asyncio.create_task(coro2(2))
    task3 = asyncio.create_task(coro2(3))
    print(await task1)
    print(await task2)
    print(await task3)

if __name__ == '__main__':
    # print(asyncio.run(coro()))
    print(asyncio.run(main3()))

# 비동기 I/O
# 이벤트 루프는 비동기 I/O를 사용해 코루틴을 실행.
# I/O 처리를 비동기로 수행하기 때문에 이벤트 루프는 다른 처리를 동시에 진행할 수 있음.
