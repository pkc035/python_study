# 220823
# 예외처리

def test():
    try:
        # 예외가 발생할 가능성이 있는 처리
        pass
    except:
        # 포착할 예외가 발생했을 때 실행할 처리
        pass
        # IndexError, TypeError 등 여러 예외 처리 가능
        # except IndexError as e:
        # raise
        # except 절 안에서는 인수 없이 raise 문을 이용할 수 있음. except절에 전달된 예외를 그대로 전송
    else:
        # 예외가 발생하지 않았을 때만 실행할 처리
        pass
    finally:
        # 예외 발생 여부와 관계없이 실행할 처리 
        # 클린업 처리에서 이용하는 구문, 예외가 발생하여도 반드시 실행할 처리를 의미
        pass
    raise ValueError
        # raise 구문을 이용해 의도적으로 예외를 발생시킬 수 있음.


# 사용자 예외 정의
# Exception 클래스를 상속해 새로운 예외를 정의 할 수 있음.

class PracticeBookError(Exception):
    pass

class PageNotFoundError(PracticeBookError):
    def __init__(self, message):
        self.message = message

class InvalidPageNumberError(PracticeBookError):
    def __init__(self, message):
        self.message = message

def test2():
    raise InvalidPageNumberError

# with
# 미리 정의도어 있는 클린업 처리를 이용할 때 사용하눈 구문
# 정의한 클린업 처리는 블록을 벗어나기 직전에 실행됨.

def test3():
    with open('test', 'w') as f:
        f.write('test')

    print(f.closed) # closed 확인 시 파일 객체가 닫혀 있음

    f = open('test','w')
    f.write('test')

    print(f.closed) # 파일 객체는 아직 닫혀있지 않음,

    f.close()
    f.closed # 파일 객체를 명시적으로 닫아줘야 파일 객체는 닫힘

    # with 문을 사용하면 파일 닫기를 잊어버리는 상황을 피할 수 있음.
    # 내장함수 open()을 사용할 때는 with 문을 사용하는게 좋음.


# 문자열
# f-string 포멧 문자열 리터럴
# 문자열 안의 변수나 식을 {}로 감싸서 결과 값 치환

# format() str 타입 메서드
# 문자열 {} str.format() 메서드 인수로 전달한 값으로 치환

# 문자열로 전환할 위치 %s, 숫자값으로 치환할 위치에 %d를 삽입
# % 연산자 이용은 가급적 피하는걸 권장....
# 포멧 연산은 여러 일반적인 오류 발생(튜플, 딕셔너리를 올바르게 표시하지 못 함)
# f-string이나 str.format(), template-strings를 사용하면 이런 오류를 피할 수 있음.

def test3():
    title = 'test'
    title_d = {'x':'test', 'y':'test2'}
    print(f'python practice {title}')
    print('python {} {}'.format('test','test'))
    print('python {} {}'.format(**title_d))


# 배열
# 변경할 수 있는 배열 list, 변경할 수 없ㄴ느 배열 tuple

# list
# 엘리먼트 추가와 삭제 list.append() list.pop()
# 인덱스로 리스트 접근, 슬라이스를 이용한 리스트 추출 list[:]

# tuple
# 정의한 후에는 엘리먼트를 변경할 수 없다.

items = ('test', 'test', 'test')

#()가 없어도 됨

items = 'test', 'test', 'test'

# dict
# 엘리먼트 추가와 삭제 가능
# 키를 통한 엘리먼트 접근 가능
items = {'test1': 1, 'test2':1, 'test3':1 }
items['test4'] = 1

del items['test1']

# items['test5'] 존재하지 않는 경우 KeyError 예외가 발생함.
# dict.get() 메소드를 이용하여 KeyError 예외 방지할 수 있음.

items.get('test1', 0)

# dict key는 문자열, 숫자값, 튜플 등.. 변경할 수 없는 객체만 가능

book = ('book',)
dic_test = {book:0}

# 리스트는 변경할 수 있는 객체이므로 Key 사용 불가

book = ['book']
# dic_test = {book:0}

# set은 엘리먼트의 중복을 허용하지 않고 순서를 유지하지 않는다.
# set.add() set.pop() set.remove() 엘리먼트를 추가 삭제가 가능

# frozenset
# set 타입과 같으나 변경할 수 없는 타입  set.add(), remove(), pop() 불가능
set_a = {'test','test2'}
set_b = {'test3','test4'}
set_c = {'test5','test6'}

# 합집합
set_a | set.b
set_a.union(set_b)

# 차집합 set.difference() 
set_b.difference(set_a)
set_b - set_a

# 교집합 
set_a.intersection(set_b)
set_a & set_b

# 대칭차집합
set_a.symmetric_difference(set_b)

# 부분집합 판정
set_a.issubset(set_b)

# 리스트컴프리헨션
# 2단,3단으로 중첩을 할 수 있으나, 중첩이 깊어지면 가독성이 급격히 떨어짐
# 리스트 컴프리헨션과 for문 중 더 간단하고 가독성이 높은 쪽을 선택

tuples = []
for x in [1,2,3]:
    for y in [4,5,6]:
        tuples.append((x,y))

tuples2 = [(x,y) for x in [1,2,3] for y in [4,5,6]]

# 길이가 변하는 인수(개수가 변하는 인수)를 받는 함수 *args
# 길이가 변하는 키워드 인수를 받는 함수 **kwargs
#  *args, **kwargs는 매우 편리한 기능이지만, 그 함수가 어떤 인수를 기대하는지 알기 어렵다.
# 코드 가독성 문제가 없는지 검토해야함.

def test4(*args, **kwrgs):
    pass

# Lambda식 이름 없는 함수를 의미하며, 함수가 필요할 때 그 즉시 정의할 수 있다.

increment = lambda num: num + 1
increment(2)

# 동일한 구문
def increment(num):
    return num + 1

# Lambda식을 너무 사용하면 코드 가독성이 떨어짐.
# 함수를 인수로 받는 함수를 호출할 때 사용.

nums = ['one', 'two', 'three']
filtered = filter(lambda x: len(x) == 3, nums)
list(filtered)

# Type 정보 부여
# 타입 정보를 부여하면 코드의 유지보수성이 높아짐.

def test5(a: int, b: str):
    pass