import numpy as np

def roll_up(matrix):
    return np.roll(matrix, -1, 0)

def roll_down(matrix):
    return np.roll(matrix, 1, 0)

def roll_left(matrix):
    return np.roll(matrix, -1, 1)

def roll_right(matrix):
    return np.roll(matrix, 1, 1)

def rot45(matrix):
    result = matrix.copy()
    pojok = result[0, 0]
    result[0, 0] = result[0, 1]
    result[0, 1] = result[0, 2]
    result[0, 2] = result[1, 2]
    result[1, 2] = result[2, 2]
    result[2, 2] = result[2, 1]
    result[2, 1] = result[2, 0]
    result[2, 0] = result[1, 0]
    result[1, 0] = pojok
    return result

if __name__ == '__main__':
    test = np.asarray([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]])
    print test
    rot45(test)
    print test
    rot45(test)
    print test
    rot45(test)
    print test
    rot45(test)
    print test
    rot45(test)
    print test
    rot45(test)
    print test
    rot45(test)
    print test