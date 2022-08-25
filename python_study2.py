#220825

#class

class Page:
    def __init__(self, num, content, section=None):
        self.num = num
        self.content = content
        self.section = section
    
    def output(self):
        return f'{self.content}'

# Page 클래스의 인스턴스별로 고유의 값이 되므로 num, content 인스턴스 변수라 함.
# output() 인스턴스 메서드라 함.

# __init__() 인스턴스 생성 직후에 자동으로 호출
# 인스턴스 초기화에 이용하며 속성을 추가하면 이 클래스의 모든 인스턴스가 그 속성을 가짐.

class Klass:
    # def __new__(cls, *args):
    #     print(f'{cls}')
    #     print('new', args)

    #     return super().__new__(cls)
    
    def __init__(self,x):
        self.__x = x
        print('init')

# __new__의 반환값은 클래스의 인스턴스, __new__() 호출한 뒤 반환값을 __init__()의 self로 전달
# __nuw__() 메서드를 사용해 인스턴스 커스터마이즈를 하는 상황은 적으며, 필요할 때 아니면 지양


class Book:
    def __init__(self, raw_price):
        if raw_price < 0:
            raise ValueError('price must be positive')
        self.raw_price = raw_price
        self._discounts = 0
    
    @property
    def discounts(self):
        return self._discounts
    
    @discounts.setter
    def discounts(self, value):
        if value < 0 or 100 < value:
            raise ValueError('discounts must be between 0 and 100')
        self._discounts = value
    
    @property
    def price(self):
        multi = 100 - self._discounts
        return int(self.raw_price * multi / 100)

# property 인스턴스 메서드에 @property를 붙이면 그 인스턴스 메서드는 ()를 붙이지 않고 호출 가능
# property가 붙은 메서드는 값을 얻을 때 호출되기 때문에 getter라고 부름
# book.discounts = 20 과 같이 값을 대입할 때 호출 되며, setter라고 부름

# _discount 인스턴스 변수의 _를 붙이 이유는 프라이빗 변수이기 때문
# __ 언더스코어 2개를 붙이면 Klass의 변수 __x를 Klass__x라는 이름으로 변환

book = Book(2000)
print(book.discounts)
print(book.price)
book.discounts = 20
print(book.price)
# book.discounts = 120

kls = Klass(10)
print(kls._Klass__x)

class Page2:
    book_title = 'python'

# 클래스 변수 를 정의 할 수 있고 값을 변경 가능
# 클래스 변수를 변경할 때는 반드시 클래스 객체를 통해 대입
# 클래스 변수는 모든 인스턴스에서 공유

Page2.book_title = 'No python'
print(Page2.book_title)

first_page = Page2()
second_page = Page2()

print(first_page.book_title)
print(second_page.book_title)

# 클래스 메서드
# 일반적으로 self가 아니라 cls라고 기술

from operator import attrgetter
class Page3:
    book_title = 'Python Book'

    def __init__(self, num, content):
        self.num = num
        self.content = content
    
    def output(self):
        return f'{self.content}'
    
    @classmethod
    def print_pages(cls, *pages):
        print(cls.book_title)
        pages = list(pages)

        for page in sorted(pages, key=attrgetter('num')):
            print(page.output())
    
    @staticmethod
    def check_blank(page):
        return bool(page.content)


first = Page3(1, 'first')
second = Page3(2, 'second page')
third = Page3(3, 'third page')

Page3.print_pages(first, third, second)
first.print_pages(first, third, second)

# 클래스 메서드 호출, 인스턴스에서도 호출 가능

# 스태틱 메서드는 일반 함수와 같다
# 스태틱 메서드를 사용할 이유는 그다지 많지 않음, 함수로 끝낼 수 있는 처리라면 함수를 만드는 편이 나음. 
page = Page3(1,'')
print(Page3.check_blank(page))

# 클래스를 정의할 때 클래스 명 뒤에 (베이스 클래스)를 붙여 상속 클래스를 정의함.

class Page4:
    def __init__(self, num, content):
        self.num = num
        self.content = content

    def output(self):
        return f'{self.content}'

class TitlePage(Page):
    def output(self):
        # 베이스 클래스의 메서드는 자동으로 호출되지 않으므로 명시적으로 호출
        title = super().output()
        return title.upper()


title = TitlePage(0, 'Python Test')
print(title.output())

# 베이스 클래스가 가진 메서드와 같은 이름의 메서드를 정의해 덮어 씌울 수 있으며 메서드 오버라이드라고 합니다.
# 베이스 클래스의 메서드를 호출할 때는 내장 함수 super()를 이용
# super()에서 반환하는 객체는 베이스 클래스에 처리를 이양하기 위한 프록시 객체


class A:
    def hello(self):
        print('A')

class B(A):
    def hello(self):
        print('B')
        super().hello()

class C(A):
    def hello(self):
        print('C')
        super().hello()

class D(B,C):
    def hello(self):
        print('D')
        super().hello()

d = D()
d.hello()

# 여러 상속원이 같은 이름의 메서드를 가지고 있을 때 경쟁을 해결해야함.
# 메서드 결정 순서는 __mro__ 속성에서 확인할 수 있음.
# 클래스 계층 구조가 깊어지거나 복잡해지면 코드 유지보수성이 낮아짐.
# 불필요한 상속은 피하고, 계층 구조는 단순하게 유지하는게 좋음.

print(D.__mro__)