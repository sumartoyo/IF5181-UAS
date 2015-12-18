import numpy as np

def roll_up(matrix, pad=0):
    result = np.roll(matrix, -1, 0)
    result[-1] = pad
    return result

def roll_down(matrix, pad=0):
    result = np.roll(matrix, 1, 0)
    result[0] = pad
    return result

def roll_left(matrix, pad=0):
    result = np.roll(matrix, -1, 1)
    result[:, -1] = pad
    return result

def roll_right(matrix, pad=0):
    result = np.roll(matrix, 1, 1)
    result[:, 0] = pad
    return result

def roll_all(matrix, pad=0):
    return (roll_up(matrix, pad), roll_down(matrix, pad), roll_left(matrix, pad), roll_right(matrix, pad))

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
    test = np.asarray([[True, False, True], [False, True, False], [False, False, False]])
    print roll_up(test)
    print roll_down(test)
    print roll_left(test)
    print roll_right(test)
    # print test
    # rot45(test)
    # print test
    # rot45(test)
    # print test
    # rot45(test)
    # print test
    # rot45(test)
    # print test
    # rot45(test)
    # print test
    # rot45(test)
    # print test
    # rot45(test)
    # print test