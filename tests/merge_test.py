from queue import Queue
GRID_LENGTH = 4
GRID_WIDTH = 4


class MergeTester:
    def __init__(self, matrix):
        self._matrix = matrix
        self._score = 0

    def print_matrix(self, title=""):
        if title:
            print(title)
        for row in self._matrix:
            print(row)
        print("-" * 30)

    def rearrange(self, column):
        queue = Queue()

        for r in range(GRID_LENGTH):
            if self._matrix[r][column] != 0:
                queue.put(self._matrix[r][column])

        r = 0
        while not queue.empty():
            self._matrix[r][column] = queue.get()
            r += 1

        while r < GRID_LENGTH:
            self._matrix[r][column] = 0
            r += 1

    def merge_column(self, col_index):
        merged_any = False

        while True:
            merged_this_pass = False

            for row_index in range(GRID_LENGTH):
                current_value = self._matrix[row_index][col_index]
                if current_value == 0:
                    continue

                for delta_row in [-1, 1]:
                    nr = row_index + delta_row
                    if (
                        0 <= nr < GRID_LENGTH
                        and
                        self._matrix[nr][col_index] == current_value
                    ):
                        self._matrix[row_index][col_index] *= 2
                        self._score += self._matrix[row_index][col_index]
                        self._matrix[nr][col_index] = 0
                        merged_this_pass = True

                for delta_col in [-1, 1]:
                    nc = col_index + delta_col
                    if (
                        0 <= nc < GRID_WIDTH
                        and
                        self._matrix[row_index][nc] == current_value
                    ):
                        self._matrix[row_index][col_index] *= 2
                        self._score += self._matrix[row_index][col_index]
                        self._matrix[row_index][nc] = 0
                        merged_this_pass = True

            self.rearrange(col_index)

            if not merged_this_pass:
                break

            merged_any = True
        return merged_any


def run_test(test_name, matrix, col):
    tester = MergeTester(matrix)
    tester.print_matrix(f"{test_name} - BEFORE")

    merged = tester.merge_column(col)

    tester.print_matrix(f"{test_name} - AFTER")
    print("Merged:", merged)
    print("Score:", tester._score)
    print("=" * 40)


run_test(
    "Vertical Merge",
    [
        [2, 8, 4, 0],
        [8, 8, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    col=0
)
