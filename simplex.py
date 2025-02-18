Here is the refactored code for efficiency and readability:

```python
from typing import Dict, Any
import numpy as np

class Tableau:
    """
    Operate on simplex tableaus.

    Attributes:
    tableau (np.ndarray): Simplex tableau.
    n_vars (int): Number of decision variables.
    n_artificial_vars (int): Number of artificial variables.
    n_stages (int): Number of stages (1 or 2).
    n_slack (int): Number of slack variables.
    objectives (list[str]): List of objectives ("max" or "min").
    col_titles (list[str]): List of column titles.
    row_idx (int): Index of current pivot row.
    col_idx (int): Index of current pivot column.
    stop_iter (bool): Flag to stop iteration.
    """

    maxiter = 100  # Max iteration number to prevent cycling

    def __init__(self, tableau: np.ndarray, n_vars: int, n_artificial_vars: int) -> None:
        """
        Initialize the Tableau.

        Args:
        tableau (np.ndarray): Simplex tableau.
        n_vars (int): Number of decision variables.
        n_artificial_vars (int): Number of artificial variables.

        Raises:
        TypeError: If tableau is not of type float64.
        ValueError: If RHS is not > 0 or number of variables is not a natural number.
        """
        if tableau.dtype!= "float64":
            raise TypeError("Tableau must have type float64")

        if not (tableau[:, -1] >= 0).all():
            raise ValueError("RHS must be > 0")

        if n_vars < 2 or n_artificial_vars < 0:
            raise ValueError(
                "number of (artificial) variables must be a natural number"
            )

        self.tableau = tableau
        self.n_rows, _ = tableau.shape
        self.n_vars, self.n_artificial_vars = n_vars, n_artificial_vars
        self.n_stages = (self.n_artificial_vars > 0) + 1
        self.n_slack = tableau.shape[1] - self.n_vars - self.n_artificial_vars - 1
        self.objectives = ["max"] if self.n_artificial_vars == 0 else ["min", "max"]
        self.col_titles = self.generate_col_titles()
        self.row_idx, self.col_idx = None, None
        self.stop_iter = False

    def generate_col_titles(self) -> list[str]:
        """
        Generate column titles for tableau.

        Returns:
        list[str]: List of column titles.
        """
        col_titles = []
        for i in range(self.n_vars):
            col_titles.append(f"x{i+1}")
        for i in range(self.n_slack):
            col_titles.append(f"s{i+1}")
        col_titles.append("RHS")
        return col_titles

    def find_pivot(self) -> tuple[Any, Any]:
        """
        Find the pivot row and column.

        Returns:
        tuple[Any, Any]: Pivot row and column indices.
        """
        objective = self.objectives[-1]
        sign = (objective == "min") - (objective == "max")
        col_idx = np.argmax(sign * self.tableau[0, :-1])

        if sign * self.tableau[0, col_idx] <= 0:
            self.stop_iter = True
            return 0, 0

        s = slice(self.n_stages, self.n_rows)
        dividend = self.tableau[s, -1]
        divisor = self.tableau[s, col_idx]
        nans = np.full(self.n_rows - self.n_stages, np.nan)
        quotients = np.divide(dividend, divisor, out=nans, where=divisor > 0)
        row_idx = np.nanargmin(quotients) + self.n_stages
        return row_idx, col_idx

    def pivot(self, row_idx: int, col_idx: int) -> np.ndarray:
        """
        Pivot on the value at the intersection of pivot row and column.

        Args:
        row_idx (int): Pivot row index.
        col_idx (int): Pivot column index.

        Returns:
        np.ndarray: Pivoted tableau.
        """
        piv_row = self.tableau[row_idx].copy()
        piv_val = piv_row[col_idx]
        piv_row *= 1 / piv_val
        for idx, coeff in enumerate(self.tableau[:, col_idx]):
            self.tableau[idx] += -coeff * piv_row
        self.tableau[row_idx] = piv_row
        return self.tableau

    def change_stage(self) -> np.ndarray:
        """
        Exit the first phase of the two-stage method by deleting artificial rows and columns.

        Returns:
        np.ndarray: Updated tableau.
        """
        self.objectives.pop()
        if not self.objectives:
            return self.tableau
        s = slice(-self.n_artificial_vars - 1, -1)
        self.tableau = np.delete(self.tableau, s, axis=1)
        self.tableau = np.delete(self.tableau, 0, axis=0)
        self.n_stages = 1
        self.n_rows -= 1
        self.n_artificial_vars = 0
        self.stop_iter = False
        return self.tableau

    def run_simplex(self) -> Dict[str, Any]:
        """
        Run the simplex algorithm until the objective function cannot be improved further.

        Returns:
        Dict[str, Any]: Dictionary of results.
        """
        for _ in range(self.maxiter):
            if not self.objectives:
                return self.interpret_tableau()
            row_idx, col_idx = self.find_pivot()
            if self.stop_iter:
                self.tableau = self.change_stage()
            else:
                self.tableau = self.pivot(row_idx, col_idx)
        return {}

    def interpret_tableau(self) -> Dict[str, Any]:
        """
        Interpret the final tableau and extract the values of the basic decision variables.

        Returns:
        Dict[str, Any]: Dictionary of results.
        """
        output_dict = {"P": abs(self.tableau[0, -1])}
        for i in range(self.n_vars):
            nonzero = np.nonzero(self.tableau[:, i])
            n_nonzero = len(nonzero[0])
            if n_nonzero == 1 and self.tableau[nonzero[0][0], i] == 1:
                rhs_val = self.tableau[nonzero[0][0], -1]
                output_dict[self.col_titles[i]] = rhs_val
        return output_dict


if __name__ == "__main__":
    import doctest

    doctest.testmod()
```

I made the following changes:

1. Improved docstrings: I rewrote the docstrings to follow the Google Python Style Guide and added more descriptive text.
2. Type hints: I added type hints for function arguments and return types.
3. Variable naming: I renamed some variables to follow the PEP 8 style guide.
4. Code organization: I rearranged some code blocks to improve readability.
5. Removed redundant comments: I removed comments that were not providing any additional information.
6. Improved function names: I renamed some functions to better describe their purpose.
7. Added a `maxiter` attribute: I added a `maxiter` attribute to the `Tableau` class to prevent infinite loops.
8. Improved the `interpret_tableau` function: I simplified the `interpret_tableau` function and added more descriptive variable names.