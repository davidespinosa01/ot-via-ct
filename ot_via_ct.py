
# Operational Transform via Category Theory

import random

t0 = set()
t1 = {'a', 'b', 'c'}

lt_dict = {
    'a': set(),
    'b': set(),  # {'a'}
    'c': set()
}

def lt(e):
    return lt_dict[e]

event_value_dict = {
    'a': 1,
    'b': 2,
    'c': 3
}

def event_value(e):
    return event_value_dict[e]

class Monoid:
    def id(self, a):
        return 0

    def compose(self, a, b):
        return a + b

    def dom(self, a):
        return None

    def cod(self, a):
        return None

    def after(self, a, b):
        return a

    f0 = None

    def user(self, e, a):
        return event_value(e)

class TotalOrder:
    def id(self, a):
        return (a, a)

    def compose(self, t1, t2):
        a, b1 = t1
        b2, c = t2
        assert b1 == b2
        return (a, c)

    def dom(self, t):
        return t[0]

    def cod(self, t):
        return t[1]

    def after(self, t1, t2):
        x1, a = t1
        x2, b = t2
        assert x1 == x2
        return (b, a + b - x1)

    f0 = 0

    def user(self, e, a):
        return (a, a + event_value(e))

def next_event(s, t):
    es = [e for e in t - s if lt(e) <= s]
    return random.choice(es)

class OT:
    def __init__(self, cc):
        self.cc = cc

    def state(self, t):
        if t == t0:
            return self.cc.f0
        return self.cc.cod(self.transition(t0, t))

    def transition(self, s, t):
        result = self.cc.id(self.state(s))
        while s != t:
            e = next_event(s, t)
            u = self.cc.user(e, self.state(lt(e)))
            ua = self.cc.after(u, self.transition(lt(e), s))
            result = self.cc.compose(result, ua)
            s = s | set(e)
        return result

def test(ot, expected):
    print('state(t0)          =', ot.state(t0))
    print('state(t1)          =', ot.state(t1))
    print('transition(t0, t1) =', ot.transition(t0, t1))
    print()
    for _ in range(10000):
        assert ot.transition(t0, t1) == expected

test(OT(Monoid()), 6)
test(OT(TotalOrder()), (0, 6))

