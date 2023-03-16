from .solutions import Solution, neutral_solution


class Cicle:
    def __init__(self, generator: Solution) -> None:
        last_length = 0
        self._generator = generator
        self._solutions = {generator}
        last_solution = generator
        while len(self._solutions) > last_length:
            last_length = len(self._solutions)
            last_solution = last_solution+generator
            if last_solution is neutral_solution:
                break
            self._solutions.add(last_solution)

    def __len__(self):
        return len(self._solutions)+1

    def __iter__(self):
        for sol in self._solutions:
            yield sol

        yield neutral_solution
