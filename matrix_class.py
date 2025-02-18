Here is the optimized code with improved readability and efficiency:

```python
from __future__ import annotations

class Matrix:
    """
    Matrix object generated from a 2D array where each element is an array representing
    a row.
    Rows can contain type int or float.
    Common operations and information available.
    """

    def __init__(self, rows: list[list[int | float]]):
        """
        Initialize a Matrix object from a 2D array.
        """
        if not rows:
            self.rows = []
            return

        if not all(isinstance(row, list) for row in rows):
            raise TypeError("Rows must be lists")

        num_cols = len(rows[0])
        if not all(len(row) == num_cols for row in rows):
            raise ValueError("All rows must have the same number of columns")

        if not all(isinstance(value, (int, float)) for row in rows for value in row):
            raise TypeError("All values must be int or float")

        self.rows = rows

    # MATRIX INFORMATION
    @property
    def num_rows(self) -> int:
        return len(self.rows)

    @property
    def num_columns(self) -> int:
        return len(self.rows[0]) if self.rows else 0

    @property
    def order(self) -> tuple[int, int]:
        return self.num_rows, self.num_columns

    @property
    def is_square(self) -> bool:
        return self.order[0] == self.order[1]

    def identity(self) -> Matrix:
        """
        Return the identity matrix of the same order.
        """
        return Matrix([[1 if i == j else 0 for j in range(self.num_rows)] for i in range(self.num_rows)])

    def determinant(self) -> int | float | None:
        """
        Calculate the determinant of the matrix.
        """
        if not self.is_square:
            return None
        if self.order == (0, 0):
            return 1
        if self.order == (1, 1):
            return self.rows[0][0]
        if self.order == (2, 2):
            return self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]
        return sum(self.rows[0][i] * self.cofactor(i, 0) for i in range(self.num_columns))

    def is_invertable(self) -> bool:
        """
        Check if the matrix is invertable.
        """
        return bool(self.determinant())

    def cofactor(self, row: int, col: int) -> int | float:
        """
        Calculate the cofactor of the element at the given row and column.
        """
        minor = self.minor(row, col)
        return minor if (row + col) % 2 == 0 else -minor

    def minor(self, row: int, col: int) -> int | float:
        """
        Calculate the minor of the element at the given row and column.
        """
        sub_matrix = [r[:col] + r[col + 1 :] for i, r in enumerate(self.rows) if i!= row]
        return Matrix(sub_matrix).determinant()

    def adjugate(self) -> Matrix:
        """
        Calculate the adjugate of the matrix.
        """
        return Matrix([[self.cofactor(j, i) for j in range(self.num_columns)] for i in range(self.num_rows)])

    def inverse(self) -> Matrix | None:
        """
        Calculate the inverse of the matrix.
        """
        det = self.determinant()
        if not det:
            return None
        return self.adjugate() * (1 / det)

    # MATRIX MANIPULATION
    def add_row(self, row: list[int | float], position: int | None = None) -> None:
        """
        Add a row to the matrix.
        """
        if len(row)!= self.num_columns:
            raise ValueError("Row must have the same number of columns as the matrix")
        if position is None:
            self.rows.append(row)
        else:
            self.rows.insert(position, row)

    def add_column(self, column: list[int | float], position: int | None = None) -> None:
        """
        Add a column to the matrix.
        """
        if len(column)!= self.num_rows:
            raise ValueError("Column must have the same number of rows as the matrix")
        if position is None:
            self.rows = [r + [column[i]] for i, r in enumerate(self.rows)]
        else:
            self.rows = [r[:position] + [column[i]] + r[position:] for i, r in enumerate(self.rows)]

    # MATRIX OPERATIONS
    def __eq__(self, other: object) -> bool:
        """
        Check if two matrices are equal.
        """
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __neg__(self) -> Matrix:
        """
        Return the negation of the matrix.
        """
        return Matrix([[-x for x in row] for row in self.rows])

    def __add__(self, other: Matrix) -> Matrix:
        """
        Add two matrices.
        """
        if self.order!= other.order:
            raise ValueError("Matrices must have the same order")
        return Matrix([[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(self.rows, other.rows)])

    def __sub__(self, other: Matrix) -> Matrix:
        """
        Subtract two matrices.
        """
        if self.order!= other.order:
            raise ValueError("Matrices must have the same order")
        return Matrix([[x - y for x, y in zip(row1, row2)] for row1, row2 in zip(self.rows, other.rows)])

    def __mul__(self, other: int | float | Matrix) -> Matrix:
        """
        Multiply the matrix by a scalar or another matrix.
        """
        if isinstance(other, (int, float)):
            return Matrix([[x * other for x in row] for row in self.rows])
        elif isinstance(other, Matrix):
            if self.num_columns!= other.num_rows:
                raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second")
            return Matrix([[sum(x * y for x, y in zip(row, col)) for col in zip(*other.rows)] for row in self.rows])
        else:
            raise TypeError("Unsupported operand type")

    def __pow__(self, other: int) -> Matrix:
        """
        Raise the matrix to a power.
        """
        if not isinstance(other, int):
            raise TypeError("Exponent must be an integer")
        if not self.is_square:
            raise ValueError("Only square matrices can be raised to a power")
        if other == 0:
            return self.identity()
        if other < 0:
            if self.is_invertable():
                return self.inverse() ** (-other)
            raise ValueError("Only invertable matrices can be raised to a negative power")
        result = self
        for _ in range(other - 1):
            result *= self
        return result

    @classmethod
    def dot_product(cls, row: list[int | float], column: list[int | float]) -> int | float:
        """
        Calculate the dot product of two vectors.
        """
        return sum(x * y for x, y in zip(row, column))

    def __str__(self) -> str:
        """
        Return a string representation of the matrix.
        """
        return '\n'.join([' '.join(map(str, row)) for row in self.rows])

if __name__ == "__main__":
    import doctest

    doctest.testmod()
```
Here's a summary of the changes:

* Improved docstrings and comments to explain the purpose and behavior of each method.
* Renamed some methods to be more descriptive and consistent with mathematical notation.
* Removed redundant code and simplified some methods.
* Improved error handling and added more informative error messages.
* Added type hints to indicate the expected types of method parameters and return values.
* Reformatted the code to be more consistent and readable.
* Added a `__str__` method to provide a string representation of the matrix.

Note that I did not make any significant changes to the mathematical algorithms or logic of the code. The changes are primarily focused on improving the code's readability, maintainability, and usability.