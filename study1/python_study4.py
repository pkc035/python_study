# 220829

# 순차 처리
# 파이썬은 의도적으로 동시 처리로 구현하지 않는 한 항상 순차 처리 수행

# 동시 처리
# 파이썬은 다중 쓰레드를 사용

# 병렬 처리
# 파이썬은 멀티 코어로 다중 프로세스를 사용
# 병렬 처리는 동시 처리이기는 하나, 동시 처리라고 해서 모두가 병렬 처리는 아님.

# 동시 처리
# CPU 바운드 처리
# 암복호화, 숫잣값 계산 등.. CPU의 자원을 사용해 계산을 수행
# 여러 코어를 동시에 사용해 병렬 처리를 할 수 있는 다중 프로세스가 유효
# GIL이 있어 다중 쓰레드, 이벤트 루프를 통한 처리 고속화는 기대할 수 없음

# I/O 바운드 처리
# 데이터베이스 접속, Web API 이용 등.. 통신에 의한 대기 시간이 발생하는 처리
# 다중 프로세스, 다중 쓰레드, 이벤트 루프 모두 유효
# 어떤 방법을 선택할지는 오버헤드나 구현 난도를 고려해서 결정


# 일반적으로 실행 시 오버헤드가 큰 순서대로 나열하면 다중 프로세스, 다중 쓰레드, 이벤트 루프 순..

# 파이썬에서는 함수나 메서드를 호출하면 호출한 대상이 처리가 되기 전까지 다음 처리를 진행하지 않음.(동기 처리)
# 호출한 대상의 결과를 얻기 전에 호출자는 다음 처리를 진행하기 때문에
# 처리 완료 알림이나 결과는 콜백 함수 등을.. 사용해 호출자에게 알림.
# 비동기 처리를 사용할 때는 동시 처리 한다고 말할 수 있음


# concurrent.futures 모듈은 동시 처리를 수행하기 위한 표준 라이브러리
# 동시 처리에서 실행할 처리를 전달하면 해당 처리를 설명할 future 객체에 캡슐화해서 비동기 처리
# 다중 쓰레드, 다중 프로레스를 거의 같은 코드로 구현 가능

# GIL 파이썬 인터프리터 전체에서 공유하는 잠금 기능. 여러 쓰레드가 있을 때,
# 여러 쓰레드가 있을 때 GIL을 얻은 하나의 쓰레드만 파이썬의 바이트 코드를 실행 할 수 있도록 설계 됨.
# 파이썬 구조 특성상 다중 쓰레드를 이요한 동시 처리에는 CPU 바운드 처리에서 빠른 속도를 기대할 수 없음.

from concurrent.futures import ThreadPoolExecutor, Future, as_completed, wait
import threading

def func():
    return 1

# 비동기로 수행할 처리를 sumit()에 전달
# future = ThreadPoolExecutor().submit(func)
# print(isinstance(future, Future))
# print(future.result())
# print(future.done())
# print(future.running())
# print(future.cancelled())

# I/O 바운드 처리에서는 다중 쓰레드화가 효과적인 선택
# I/O를 수반한 처리는, 하드웨어나 네트워크 등.. 외부 환경에 의존적임.
# 프로그램을 변경해도 개별적인 처리 속도의 증가를 기대하기 어렵.

# 여러 처리를 할 때는 비동기 실행으로 동시화하면 통신 중 대기 시간을 효과적으로 활용하여 전체 시간을 단축.,
# 다중 프로세스 처리에서도 전체 시간을 단축할 수 있지만, 쓰레드는 프로세스보다 오버헤드가 작다는 장점.

urls = [
    'https://twitter.com',
    'https://facebook.com',
    'https://instagram.com'
]

from hashlib import md5
from pathlib import Path
from urllib import request

def download(url):
    req = request.Request(url)

    name = md5(url.encode('utf-8')).hexdigest()
    file_path = './' + name

    with request.urlopen(req) as res:
        Path(file_path).write_bytes(res.read())
        return url, file_path

import time

def elapsed_time(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        v = f(*args, **kwargs)
        print(f"{f.__name__}: {time.time() - start}")
        return v
    return wrapper

@elapsed_time
def get_squential():
    for url in urls:
        print(download(url))

@elapsed_time
def get_multi_thread():
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(download, url): url for url in urls}
        
        for future in as_completed(futures):
            # 완료된 것부터 얻음
            print(future.result())


get_squential()
get_multi_thread()

# as_completed() 함수는 처리를 완료한 것부터 순서대로 반환
# result()를 호출하면 효율적인 결과를 얻어냄, 만약 에러 발생시 result()도 예외 발생함.

class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count = self.count + 1

def count_up(counter):
    for _ in range(1000000):
        counter.increment()

counter = Counter()
threads = 2

with ThreadPoolExecutor() as e:
    futures = [e.submit(count_up, counter) for _ in range(threads)]
    done, not_done = wait(futures)

print(f'{counter.count=:,}')

# 두개의 쓰레드가 각각 1,000,000 번씩 카운터를 증가 시킴
# 단, 쓰레드 세이프한 구현이 아니기 때문에 처리 완료 후 카운터의 값이 2,000,000이 안됨.
# self.count 두 개의 쓰레가 동시에 접근하는 상황이 발생해 간섭을 일으킬 수 있는 상태가 됨.
# 여러 쓰레드가 동시에 같으 객체에 접근하면 예상대로 동작하지 않을 수 있으므로 위험.

# threading.lock 객체를 이용하여 Lock을 통해 배타 제어 exclusive control를 삽입.
# 특정 한 쓰레드가 Lock을 취득하면 해당 Lock이 해제될 때까지 다른 쓰레드는 Lock을 얻을 수 없음.
# 배타 제어를 수행할 위치에서 록을 얻은 뒤 처리가 끝나면 빠르게 Lock을 해제
# 뒤늦게 해제되는 상황을 방지하기 위해 Lock 객체는 with 문과 함께 사용.

class ThreadSafeCounter:
    lock = threading.Lock()
    def __init__(self):
        self.count = 0
    
    def increment(self):
        # 배타 제어할 처리를 Lock 안에 씀
        with self.lock:
            self.count = self.count + 1

counter = ThreadSafeCounter()
threads = 2

with ThreadPoolExecutor() as e:
    futures = [e.submit(count_up, counter) for _ in range(threads)]
    done, not_done = wait(futures)

print(f'{counter.count=:,}')
