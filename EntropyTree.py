import math
import numpy as np

cord_glob = []
tree = []


class Node:
    def __init__(self, left, right, cord):
        self.left = left
        self.right = right
        self.cord = cord
        self.leaf = None
        self.label = -1
        self.success_count = 0

    # took print tree from here
    # https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python

    # print tree

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        # No child.
        if self.right is None and self.left is None:
            line = str(self.cord)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = str(self.cord)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def entropy_recursion(k, node, vec, labels):
    if k == 0:
        count_zero = 0
        count_one = 0

        for key, v in vec.items():
            if labels[key] == 0:
                count_zero = count_zero + 1
            if labels[key] == 1:
                count_one = count_one + 1

        if count_one > count_zero:
            cord = 1
        else:
            cord = 0

        tree.append(cord)
        node.cord = cord
        node.leaf = cord
        return node

    max_split = math.inf
    cord_split = -1
    for j in range(8):
        if j not in cord_glob:
            temp = check_entropy(vec, labels, j)
            if temp < max_split:
                max_split = temp
                cord_split = j

    cord_glob.append(cord_split)
    tree.append(cord_split)

    node.cord = cord_split
    vec_right = vec.copy()
    vec_left = vec.copy()
    for key, v in vec.items():
        if v[cord_split] != 0:
            del vec_left[key]
        else:
            del vec_right[key]

    node.left = entropy_recursion(k - 1, Node(None, None, -1), vec_left, labels)
    node.right = entropy_recursion(k-1, Node(None, None, -1), vec_right, labels)

    return node


def create_entropy(k, vec, labels):
    root = Node(None, None, -1)
    t = entropy_recursion(k-1, root, vec, labels)
    return t


# check by this func = -plog2(p) - (1-p)log2(1-p)
def check_entropy (vec, labels, cord):
    count_one_zero = 0
    count_total_zero = 0
    count_one = 0
    count_total_one = 0

    for k, v in vec.items():
        if v[cord] == 0:
            count_total_zero = count_total_zero + 1
            if labels[k] == 1:
                count_one_zero = count_one_zero + 1
        else:
            count_total_one = count_total_one + 1
            if labels[k] == 1:
                count_one = count_one + 1

    p_zero = count_one_zero/count_total_zero
    p_one = count_one/count_total_one
    entropy_zero = (-p_zero * np.log2(p_zero)) - ((1 - p_zero) * np.log2(1 - p_zero))
    entropy_one = (-p_one * np.log2(p_one)) - ((1 - p_one) * np.log2(1 - p_one))
    return entropy_zero + entropy_one


def calculate_err_entropy (vec, labels, t):
    count_err = 0
    for key, v in vec.items():
        temp_node = t
        while temp_node.leaf is None:
            if v[temp_node.cord] == 0:
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right
        if labels[key] != temp_node.cord:
            count_err = count_err + 1

    return count_err/150
