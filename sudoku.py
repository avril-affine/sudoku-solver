
class Cell(object):

    def __init__(self, board, posx, posy, val, num_candidates=9):
        self.board = board
        self.posx = posx
        self.posy = posy
        self.val = val
        self.num_candidates = num_candidates
        
        # setup candidates
        if self.val == 0:
            self.candidates = set(range(1, num_candidates+1))
            self.fixed = False
        else:
            self.candidates = {val}
            self.fixed = True


    def __len__(self):
        return len(self.candidates)

    def __repr__(self):
        return str(self.val)

    def get_val(self):
        return self.val

    def set_val(self, val):
        self.val = val
        if val != 0:
            self.candidates = {val}
        else:
            self.candidates = set(range(1, self.num_candidates+1))

    def is_unique(self):
        return len(self.candidates) == 1

    def is_fixed(self):
        return self.fixed

    def remove_candidate(self, val):
        """Attempts to remove candidate
        check if fixed

        Returns tuple or bool: Maybe fix to cleaner solution later
        """
        if self.is_fixed():
            return True         # nothing to do so possible

        if val in self.candidates:
            self.candidates.remove(val)
            if self.is_unique():
                num = list(self.candidates)[0]
                self.val = num
                return (num, self.posx, self.posy)  # update at end
            if len(self.candidates) == 0:
                return False    # move not possible

        return True             # nothing to do so possible

    def add_candidate(self, val):
        """Attempts to add candidate to cell

        Return bool: True if no other cells need to be updated.
                     False otherwise.
        """
        if self.is_fixed() or val in self.candidates:
            return True

        # check if can add val to candidates
        check = self.board.row_contains_val(val, self.posx, self.posy) | \
                self.board.col_contains_val(val, self.posx, self.posy) | \
                self.board.box_contains_val(val, self.posx, self.posy)
        
        if check:
            return True         # nothing needs to be added

        start = self.is_unique()
        self.candidates.add(val)
        return not start


class Board(object):
    
    def __init__(self, grid, num_boxes=3):
        self.size = len(grid[0])
        self.grid = [[] for _ in xrange(self.size)]
        for i in xrange(self.size):
            for j in xrange(self.size):
                val = int(grid[i][j])
                self.grid[i].append(Cell(self, i, j, val))
        self.num_boxes = num_boxes

        print '-------Starting Board------'
        print self

        # update empty cells
        for i in xrange(self.size):
            for j in xrange(self.size):
                val = self.grid[i][j].get_val()
                if val != 0:
                    res = self.make_move(val, i, j)
                    if not res:
                        raise Exception('Invalid Board')

        # for i in xrange(self.size):
        #     for j in xrange(self.size):
        #         print i, j, self.grid[i][j].fixed

    def __repr__(self):
        out = ""
        for i in xrange(9):
            line = ""
            for j in xrange(9):
                if j != 0 and j % 3 == 0:
                    line += ' | '
                cell = self.grid[i][j].get_val()
                if cell == 0:
                    line += "_"
                else:
                    line += str(cell)
            if i != 0 and i % 3 == 0:
                out += '-' * 15 + '\n'
            out += line + "\n"
        return out


    def update_candidates(self, num, i, j, fwd):
        """Updates rows, columns, and grid
        t 
        Make sure to update all current cells before updating cells 
        that were set

        Returns bool. True if valid update, False otherwise.
        """
        if fwd:
            self.grid[i][j].set_val(num)
        else:
            num = self.grid[i][j].get_val()
            self.grid[i][j].set_val(0)

        update_vals = []
        for k in xrange(self.size):         # row
            if k == j:
                continue
            if fwd:
                res = self.grid[i][k].remove_candidate(num)
            else:
                res = self.grid[i][k].add_candidate(num)

            if isinstance(res, tuple):
                update_vals.append(res)
            elif not res:
                return False

        for k in xrange(self.size):         # col
            if k == i:
                continue
            if fwd:
                res = self.grid[k][j].remove_candidate(num)
            else:
                res = self.grid[k][j].add_candidate(num)

            if isinstance(res, tuple):
                update_vals.append(res)
            elif not res:
                return False

        i_start = (i / self.num_boxes) * self.num_boxes
        j_start = (j / self.num_boxes) * self.num_boxes
        for ki in xrange(i_start, i_start + self.num_boxes):        # box
            for kj in xrange(j_start, j_start + self.num_boxes):
                if ki == i and kj == j:
                    continue
                if fwd:
                    res = self.grid[ki][kj].remove_candidate(num)
                else:
                    res = self.grid[ki][kj].add_candidate(num)

                if isinstance(res, tuple):
                    update_vals.append(res)
                elif not res:
                    return False

        # update all other cells that got set
        res = [self.update_candidates(x,y,z,fwd) for x,y,z in update_vals]    

        if res:
            return reduce(lambda x,y: x & y, res)
        else:
            return True

    # def unupdate_candidates(self, num, i, j):
    #     """Clears cell (i, j)
    #     Recursively call if adding value causes it to be len > 1
    #     """
    #     #TODO
    #     pass

    def make_move(self, num, i, j):
        """Tries to place num in cell (i, j)
        """
        return self.update_candidates(num, i, j, fwd=True)

    def unmake_move(self, i, j):
        """Clears cell (i, j)
        Recursively call if adding value causes it to be len > 1
        """
        self.update_candidates(0, i, j, fwd=False)

    def is_a_solution(self):
        """Checks for a valid solution
        """
        res = True
        for i in xrange(self.size):
            for j in xrange(self.size):
                res = res & (self.grid[i][j].is_unique() == 1)
        return res

    def next_move(self):
        """Finds next move based on least ammount of candidates
        """
        min_candidates = self.size + 1
        best_i = -1
        best_j = -1
        for i in xrange(self.size):
            for j in xrange(self.size):
                if self.grid[i][j].is_fixed():
                    continue
                n = len(self.grid[i][j])
                if n < min_candidates and n != 1:
                    best_i = i
                    best_j = j
        if len(self.grid[best_i][best_j].candidates) == 0:
            raise Exception('Zero candidates')
        return best_i, best_j

    def row_contains_val(self, num, i, j):
        res = False
        for k in xrange(self.size):
            if k == j:
                continue
            res = res | self.grid[i][k].get_val() == num
        return res

    def col_contains_val(self, num, i, j):
        res = False
        for k in xrange(self.size):
            if k == i:
                continue
            res = res | self.grid[k][j].get_val() == num
        return res
    
    def box_contains_val(self, num, i, j):
        res = False
        i_start = (i / self.num_boxes) * self.num_boxes
        j_start = (j / self.num_boxes) * self.num_boxes
        for ki in xrange(i_start, i_start + self.num_boxes):
            for kj in xrange(j_start, j_start + self.num_boxes):
                if ki == i and kj == j:
                    continue
                res = res | self.grid[ki][kj].get_val() == num
        return res 


def find_solution(board):

    if board.is_a_solution():
        print '------Solution------'
        print board
        return True
    else:
        i,j = board.next_move()
        for num in board.grid[i][j].candidates:
            # check if move is possible
            if not board.update_candidates(num, i, j):
                board.unupdate_candidates(i, j)             
                continue
            outcome = find_solution(board)
            board.unupdate_candidates(i, j)
            if outcome:
                return True
    return False

if __name__ == '__main__':
    grid = []
    with open('easy.txt', 'r') as f:
        for line in f:
            grid.append(line.strip())
    board = Board(grid)
    find_solution(board)
