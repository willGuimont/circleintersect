import numpy as np


def circle_intersect(c1, r1, c2, r2, lr='lr'):
    """
    Function to return the intersection points between two circles given their centres and radii.
    Port of Peter Kovesi's circleintersect.m (https://www.peterkovesi.com/matlabfns/)
    :param c1: center of circle 1
    :param r1: radius of circle 1
    :param c2: center of circle 2
    :param r2: radius of circle 2
    :param lr: 'lr' for both solutions,
                'l' for solution to the left of the line from c1 to c2,
                'r' or solution to the right of the line from c1 to c2
    :return: (intersection 1, intersection 2)
    """
    maxmag = max(r1, r2, *c1, *c2)
    eps = np.finfo(np.float).resolution
    tolerance = 100 * (maxmag + 1) * eps

    base_line = c2 - c1
    distance = np.linalg.norm(base_line)

    # infinite number of solutions
    if distance < eps and abs(r1 - r2) < tolerance:
        i1 = c1 + np.array([r1, 0])
        return i1, i1

    base_line = base_line / distance  # normalise
    base_line_perp = np.array([-base_line[1], base_line[0]])

    # degenerate cases
    if r1 < tolerance and abs(distance - r2) < tolerance:
        i1 = c1
        return i1, i1
    elif r2 < tolerance and abs(distance - r1) < tolerance:
        i1 = c2
        return i1, i1

    # triangle inequality
    if distance > (r1 + r2) or r1 > (distance + r2) or r2 > (distance + r1):
        raise Exception('No solution to circle intersection')

    # normal solutions
    cos_r2 = (distance ** 2 + r1 ** 2 - r2 ** 2) / (2 * distance * r1)
    sin_r2 = np.sqrt(1 - cos_r2 ** 2)

    if lr == 'lr':
        i1 = c1 + r1 * cos_r2 * base_line + r1 * sin_r2 * base_line_perp
        i2 = c1 + r1 * cos_r2 * base_line - r1 * sin_r2 * base_line_perp
    elif lr == 'l':
        i1 = c1 + r1 * cos_r2 * base_line + r1 * sin_r2 * base_line_perp
        i2 = []
    elif lr == 'r':
        i1 = c1 + r1 * cos_r2 * base_line - r1 * sin_r2 * base_line_perp
        i2 = []
    else:
        raise Exception('illegal left/right solution request')
    return i1, i2


if __name__ == '__main__':
    i1, i2 = circle_intersect(np.array([0, 0]), 2, np.array([1, 1]), 3)
    print(i1, i2)
