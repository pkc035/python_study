# 220827

# 제너레이터
# 리스트나 튜플처럼 for 문에서 사용할 수 있는 이터러블 객체
# 리스트나 튜플은 모든 엘리먼트를 메모리에 유지하기 때문에 메모리 사용량이 커지는 단점
# 제너레이터는 다음 엘리먼트가 필요한 순간에 새로운 엘리먼트를 생성해서 반환, 엘리먼트 수에 관계없이 메모리 사용량 적게 유지

from email import iterators
from re import L


def inf(n):
    while True:
        yield n

# for i in inf(3):
#     print(i)

# 제너레이터 함수를 사용, 제너레이터 식을 사용

def gen_function(n):
    print('start')

    while n:
        print(f'yield:{n}')
        yield n
        n -= 1

gen = gen_function(2)
# next(gen)
# next(gen)
# next(gen)
# StopIteration 예외가 발생할 때까지 __next__()를 계속 호출

print([i for i in gen_function(5)])
print(max(gen_function(5)))
# for 문이나 컴프리헨션, 인수에 사용 가능

x = [1, 2, 3, 4, 5]

# 리스트컴프리헨션
listcomp = [i**2 for i in x]
print(listcomp) # 모든 엘리먼트가 메모리에 할당됨

# 제너레이터 식
gen = (i**2 for i in x)
print(list(gen)) # 각 엘리먼트는 필요할 때까지 계산되지 않음

# 제너레이터 내부에서 추가로 제너레이터를 만들때 yield from 식을 사용

def chain(iterables):
    for iterable in iterables:
        for v in iterable:
            yield v

iterables = ('python', 'book')
print(list(chain(iterables)))


def chain2(iterables):
    for iterable in iterables:
        yield from (v for v in iterable)

print(list(chain2(iterables)))

# len()은 제너레이터에 사용할 수 없음, list, tuple로 변환하여 사용 가능

# 제너레이터 사례 예시
# 파일 내용을 대문자로 변환하는 프로그램.
# 읽기 -> 변환 -> 쓰기 과정을 한 행씩 수행하기 때문에 파일의 크기가 아무리 크더라도 메모리 부하가 적음

def reader(src):
    with open(src) as f:
        for line in f:
            yield line

def convert(line):
    return line.upper()

def writer(dest, reader):
    with open(dest, 'w') as f:
        for line in reader:
            f.write(convert(line))

writer('dest.txt', reader('src.txt'))

# 제너레이터는 값을 무한히 변환하거나 큰 데이터를 다루고자 할때 발휘
# 데이터 분석이나 머신러닝 등.. 대량의 텍스트 데이터나 이미지 파일을 많이 다룸

# 데코레이터

def deco1(f):
    print('deco1 called')

    def wrapper():
        print('before exec')
        v = f()
        print('after exec')
        return v
    
    return wrapper


@deco1
def func():
    print('exec')
    return 1

func()

# 인수를 받는 함수 데코레이터

def deco2(f):
    def wrapper(*args, **kwargs):
        print('before exec')
        v = f(*args, **kwargs)
        print('after exec')
        return v
    return wrapper



# 데코레이터 자체가 인수를 받는 데코레이터

def deco3(z):
    def _deco3(f):
        def wrapper(*args, **kwargs):
            print('before exec', z)
            v = f(*args, **kwargs)
            print('after exec', z)
            return v
        return wrapper
    return _deco3

#데코레이터를 붙일 때는 안쪽 데코레이터부터 적용

@deco3(z=3)
@deco3(z=4)
def func(x,y):
    print('exce')
    return x,y

print(func(1,2))

from functools import wraps
import time

def elapsed_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        v = f(*args, **kwargs)
        print(f"{f.__name__}: {time.time() - start}")
        return v
    return wrapper

@elapsed_time
def func(n):
    return sum(i for i in range(n))

print(func(100))

