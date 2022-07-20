import random as r


class Tile:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.possibilities = list(self.grid.initial_possibilities)
        self.entropy = len(self.possibilities)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def collapse(self):
        self.possibilities = [r.choice(self.possibilities)]
        self.grid.collapsed.append(self)

    def upd_information(self):
        allowed = []
        disallowed = []
        for i in self.possibilities:
            for j in self.grid.connections[i]:
                allowed.append(j)
        allowed = list(set(allowed))
        for k in range(self.grid.num_pos):
            if k not in allowed:
                disallowed.append(k)

        return disallowed
