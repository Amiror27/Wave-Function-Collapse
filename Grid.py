import random as r
from Tile import Tile


class Grid:
    def __init__(self, x_size, y_size, num_pos, connections):
        self.x_size, self.y_size, self.num_pos = x_size, y_size, num_pos
        self.initial_possibilities = [i for i in range(num_pos)]
        self.map = [[Tile(j, i, self) for j in range(self.x_size)] for i in range(self.y_size)]
        self.queue, self.blacklist, self.collapsed = [], [], []
        self.connections = connections
    
    def __repr__(self):
        return str(self.map)

    def lowest_uncollapsed_entropy(self):
        bottom = self.num_pos
        for i in range(self.y_size):
            for j in range(self.x_size):
                l = self.map[i][j].entropy
                if bottom > l > 1:
                    bottom = l

        return bottom

    def tiles_with_entropy(self, bottom, top=None):
        top = top if top is not None else bottom
        tiles = []
        for i in range(self.y_size):
            for j in range(self.x_size):
                l = self.map[i][j].entropy
                if top >= l >= bottom:
                    tiles.append(self.map[i][j])
        return sorted(tiles, key=lambda t: t.entropy)

    def upd_neighbors(self, x, y):
        removed = self.map[y][x].upd_information()
        updated = []

        for i in removed:
            if y > 0 and i in self.map[y-1][x].possibilities:
                self.map[y-1][x].possibilities.remove(i)
                updated.append(self.map[y-1][x])

            if x < self.x_size-1 and i in self.map[y][x+1].possibilities:
                self.map[y][x+1].possibilities.remove(i)
                updated.append(self.map[y][x+1])

            if y < self.y_size-1 and i in self.map[y+1][x].possibilities:
                self.map[y+1][x].possibilities.remove(i)
                updated.append(self.map[y+1][x])

            if x > 0 and i in self.map[y][x-1].possibilities:
                self.map[y][x-1].possibilities.remove(i)
                updated.append(self.map[y][x-1])
        
        return list(set(updated))

    def sub_iteration(self):
        for i in self.blacklist:
            if i in self.queue:
                self.queue.remove(i)

        if len(self.queue) > 0:
            cur = self.queue[0]
            cur.upd_neighbors()

    def single_iteration(self):
        determined = [i for i in self.tiles_with_entropy(1) if i not in self.collapsed]
        if len(determined) > 0:
            origin = r.choice(determined)
        else:
            options = self.tiles_with_entropy(self.lowest_uncollapsed_entropy())
            origin = r.choice(options)

        origin.collapse()
        self.upd_neighbors(origin.x, origin.y)
        self.blacklist = []
        self.queue = self.tiles_with_entropy(2, self.num_pos - 1)
        while len(self.queue) > 0:
            self.sub_iteration()
            self.queue = [i for i in self.tiles_with_entropy(2, self.num_pos - 1) if i not in self.blacklist]
        
    @property    
    def possibilities_of_each_tile(self):
        options_list = []
        for i in range(self.y_size):
            for j in range(self.x_size):
                options_list.append(self.map[i][j].possibilities)
        
        return options_list
