class NeutralSolution:
    def __add__(self, other: "Solution"):
        return other

    def __iter__(self):
        yield None

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, NeutralSolution)


neutral_solution = NeutralSolution()


class Solution:
    def __init__(self, x: int, y: int, a: int, prime: int) -> None:
        self._x = x
        self._y = y
        self._a = a
        self._prime = prime

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __add__(self, other:  "Solution") -> "Solution":
        if other is neutral_solution:
            return self

        if self.x == other.x:
            if self.y == -1*other.y:
                return neutral_solution

            constant = (3*self.x**2+self._a)*pow((2*self.y), -1, self._prime)

        else:
            constant = (other.y-self.y)*pow((other.x-self.x), -1, self._prime)

        new_x = constant**2-self.x-other.x
        return Solution(new_x % self._prime, (constant*(self.x-new_x)-self.y) % self._prime, self._a, self._prime)

    def __str__(self):
        return f'Solution{{ x={self._x}, y={self._y}, a={self._a}, prime={self._prime} }}'

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Solution):
            return self.x == __o.x and self.y == __o.y
        return False

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __mul__(self, factor: int):
        sol = self
        for _ in range(factor-1):
            sol += self
        return sol
