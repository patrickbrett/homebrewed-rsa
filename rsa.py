from collections import Counter

"""
calculates x^a mod m
"""
def modular_exponentiate(x, a, m):
    curr = 1
    for i in range(a):
        curr = (x * curr) % m
    return curr


"""
faster algorithm to calculate x^a mod m
"""
def modular_exponentiate_by_squaring(x, a, m):
    if m == 1:
        return 0
    curr = 1
    x = x % m
    while a > 0:
        if a % 2 == 1:
            curr = (x * curr) % m
        a >>= 1
        x = (x * x) % m
    return curr


"""
Helper for running the extended Euclidean algorithm
"""
class LinearSum:
    """
    Represents a0 * a1 + b0 * b1
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b


    def __repr__(self):
        return(f"({self.a[0]} * {self.a[1]} + {self.b[0]} * {self.b[1]})")


    """
    Recursively parses the expression to solve the linear Diophantine equation
    """
    def count(self):
        count = Counter()

        for cont, mul in [self.a, self.b]:
            if isinstance(cont, LinearSum):
                temp_count = cont.count()
                for k in temp_count.keys():
                    count[k] += mul * temp_count[k]
            else:
                count[cont] += mul

        return count


class Cryptor:
    def __init__(self, p, q, e = 3):
        self.p = p
        self.q = q
        self.e = e
        self.tot = (p - 1) * (q - 1)
        self.n = p * q
        self.d = self.find_d(self.e, self.tot)
    

    """
    Finds private key given public key and totient
    """
    def find_d(self, e, tot):
        print(e, tot)
        larger, smaller = max([e, tot]), min([e, tot])

        mem = {}
        while smaller > 1:
            div = larger // smaller
            rem = larger % smaller

            mem[rem] = LinearSum((larger, 1), (smaller, -1 * div))

            larger, smaller = smaller, rem
        
        for k in reversed(sorted(mem.keys())):
            a0, a1 = mem[k].a[0], 1
            b0, b1 = mem[k].b

            if a0 in mem:
                a0 = mem[a0]
            if b0 in mem:
                b0 = mem[b0]

            a = a0, a1
            b = b0, b1

            mem[k] = LinearSum(a, b)

        counts = mem[1].count()
        return counts[e] % tot


if __name__ == '__main__':
    Cryptor(5, 11, 7)
