class A:
    def __init__(self, a):
        self.a = a


class B:
    def __init__(self, b):
        self.b = b

class Me:
    def __init__(self, a: A, b: B):
        self.a = a
        self.b = b

    def __str__(self):
        return f'Me: a = {self.a.a}  b = {self.b.b}'




if __name__ == '__main__':
    a = A(a=1)
    b = B(b=2)

    me = Me(a, b)
    me2 = Me(a, b)
    print(me)
    me.a.a = 10
    print(me)
    print(me2)