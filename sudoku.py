import sys
import math


class Board(object):
    def __init__(self, grid):
        self.size = len(grid[0])
        self.num_boxes = int(math.sqrt(self.size))
        self.grid = []
        self.fixed = []
        self.visited = []
        for i in xrange(self.size):
            line = []
            line_fixed = []
            line_visited = []
            for j in xrange(self.size):
                val = int(grid[i][j])
                line.append(val)
                line_fixed.append(val != 0)
                line_visited.append(val != 0)
            self.grid.append(line)
            self.fixed.append(line_fixed)
            self.visited.append(line_visited)

    def __repr__(self):
        out = ""
        for i in xrange(self.size):
            line = ""
            for j in xrange(self.size):
                if j != 0 and j % self.num_boxes == 0:
                    line += ' | '
                val = self.grid[i][j]
                cell = str(val) if val != 0 else '_'
                line += cell
            if i != 0 and i % self.num_boxes == 0:
                out += '-' * (self.size + (self.size/self.num_boxes-1)*3)
                out += '\n'
            out += line + '\n'
        return out

    def is_a_solution(self):
        for i in xrange(self.size):
            for j in xrange(self.size):
                if self.grid[i][j] == 0:
                    return False
        return True

    def make_move(self, num, i, j):
        if self.fixed[i][j] or self.visited[i][j]:
            raise Exception('Trying to fill a fixed or visited cell')
        self.grid[i][j] = num
        self.visited[i][j] = True

    def unmake_move(self, i, j):
        if self.fixed[i][j] or not self.visited[i][j]:
            raise Exception('Trying to fill a fixed or unvisited cell')
        self.grid[i][j] = 0
        self.visited[i][j] = False

    def next_move(self):
        min_candidates = self.size + 1
        for i in xrange(self.size):
            for j in xrange(self.size):
                if self.fixed[i][j] or self.visited[i][j]:
                    continue
                candidates = set()
                for val in xrange(1, self.size+1):
                    if self.is_candidate(val, i, j):
                        candidates.add(val)
                if len(candidates) == 0:
                    return False            # board not possible
                if len(candidates) < min_candidates:
                    best_i = i
                    best_j = j
                    best_candidates = candidates
                    min_candidates = len(candidates)
        return best_candidates, best_i, best_j

    def is_candidate(self, num, i, j):

        for k in xrange(self.size):
            if k == j:
                continue
            if self.grid[i][k] == num:
                return False

        for k in xrange(self.size):
            if k == i:
                continue
            if self.grid[k][j] == num:
                return False
    
        i_start = (i / self.num_boxes) * self.num_boxes
        j_start = (j / self.num_boxes) * self.num_boxes
        for ki in xrange(i_start, i_start + self.num_boxes):
            for kj in xrange(j_start, j_start + self.num_boxes):
                if ki == i and kj == j:
                    continue
                if self.grid[ki][kj] == num:
                    return False
        return True


def find_solution(board):

    if board.is_a_solution():
        print '------Solution------'
        print board
        return True
    else:
        move = board.next_move()
        if not move:
            return False
        candidates,i,j = move
        for num in candidates:
            board.make_move(num, i, j)
            outcome = find_solution(board)
            board.unmake_move(i, j)
            if outcome:
                return True
    return False

if __name__ == '__main__':
    grid = []
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
    else:
        print 'Specify test file path'
        sys.exit()

    with open(input_file, 'r') as f:
        for line in f:
            grid.append(line.strip())
    board = Board(grid)
    print '------Starting Board------'
    print board
    find_solution(board)

