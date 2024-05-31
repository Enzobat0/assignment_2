import sys

class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, matrixFilePath=None):
        self.matrix = {}
        if matrixFilePath:
            self.load_matrix_from_file(matrixFilePath)
        else:
            self.rows = numRows
            self.cols = numCols

    def load_matrix_from_file(self, matrixFilePath):
        try:
            with open(matrixFilePath, 'r') as file:
                lines = file.readlines()
        
            if not lines[0].strip().startswith("rows=") or not lines[1].strip().startswith("cols="):
                raise ValueError("File must start with rows= and cols= lines")

            self.rows = int(lines[0].strip().split('=')[1])
            self.cols = int(lines[1].strip().split('=')[1])
        
            for line in lines[2:]:
                line = line.strip()
                if line:
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError(f"Line format is incorrect: {line}")
                    try:
                        row, col, value = map(int, line[1:-1].split(','))
                        self.setElement(row, col, value)
                    except Exception as e:
                        raise ValueError(f"Error parsing line: {line}") from e
        except Exception as e:
            raise ValueError(f"Input file has wrong format: {e}") from e

    def getElement(self, currRow, currCol):
        return self.matrix.get(currRow, {}).get(currCol, 0)

    def setElement(self, currRow, currCol, value):
        if currRow not in self.matrix:
            self.matrix[currRow] = {}
        self.matrix[currRow][currCol] = value

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must agree")
        result = SparseMatrix(self.rows, self.cols)
        for row in self.matrix:
            for col in self.matrix[row]:
                result.setElement(row, col, self.getElement(row, col) + other.getElement(row, col))
        for row in other.matrix:
            for col in other.matrix[row]:
                if (row not in self.matrix) or (col not in self.matrix[row]):
                    result.setElement(row, col, other.getElement(row, col))
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must agree")
        result = SparseMatrix(self.rows, self.cols)
        for row in self.matrix:
            for col in self.matrix[row]:
                result.setElement(row, col, self.getElement(row, col) - other.getElement(row, col))
        for row in other.matrix:
            for col in other.matrix[row]:
                if (row not in self.matrix) or (col not in self.matrix[row]):
                    result.setElement(row, col, -other.getElement(row, col))
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions must agree for multiplication")
        result = SparseMatrix(self.rows, other.cols)
        for row in self.matrix:
            for col in self.matrix[row]:
                if col in other.matrix:
                    for inner_col in other.matrix[col]:
                        result.setElement(row, inner_col,
                                          result.getElement(row, inner_col) +
                                          self.getElement(row, col) * other.getElement(col, inner_col))
        return result

def main():
    try:
        operation = input("Enter the matrix operation (add, subtract, multiply): ").strip().lower()
        file1 = input("Enter the path to the first matrix file: ").strip()
        file2 = input("Enter the path to the second matrix file: ").strip()
        matrix1 = SparseMatrix(matrixFilePath=file1)
        matrix2 = SparseMatrix(matrixFilePath=file2)
        if operation == 'add':
            result = matrix1.add(matrix2)
        elif operation == 'subtract':
            result = matrix1.subtract(matrix2)
        elif operation == 'multiply':
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid operation")
        
        output_file = input("Enter the output file path: ").strip()
        with open(output_file, 'w') as f:
            f.write(f"rows={result.rows}\n")
            f.write(f"cols={result.cols}\n")
            for row in result.matrix:
                for col in result.matrix[row]:
                    f.write(f"({row}, {col}, {result.getElement(row, col)})\n")
        print("Operation completed successfully. Check the output file for results.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()