
class Node:
    def __init__(self, left, right, cord):
        self.left = left
        self.right = right
        self.cord = cord
        self.label = -1
        self.success_count = 0
        self.leaf = None

    # took print tree from here
    # https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python

    # print tree
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.label
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.cord
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


def brute_force(k, vec, labels):
    path_tup = []
    if k == 0:
        return None
    t = brute_force_recursive(k - 1, vec, labels, path_tup, None)
    return t


def check_best (k, vec, labels, path_tup, flag):
    best_success = 0
    best_root = None
    left = None
    right = None
    for i in range(8):
        tup = (i, 0)
        tup_2 = (i, 1)
        if flag == 1:
            left = make_leaves(vec, labels, path_tup.copy(), tup)
            right = make_leaves(vec, labels, path_tup.copy(), tup_2)
        if flag == 2:
            left = brute_force_recursive(k - 1, vec, labels, path_tup.copy(), tup)
            right = brute_force_recursive(k - 1, vec, labels, path_tup.copy(), tup_2)
        sum_it = 0
        if left is not None:
            sum_it += left.success_count
        if right is not None:
            sum_it += right.success_count
        if best_success < sum_it:
            best_root = Node(left, right, i)
            best_root.success_count = sum_it
            best_success = best_root.success_count
    return best_root


def brute_force_recursive(k, vec, labels, path_tup, check_cord):
    if check_cord is not None:
        path_tup.append(check_cord)
    if k == 1:
        best = check_best(k, vec, labels, path_tup.copy(), 1)
        return best
    else:
        best = check_best(k, vec, labels, path_tup.copy(), 2)
        return best


def make_leaves(vec, labels, path_tup, check_cord):
    count_one = 0
    count_zero = 0
    path_tup.append(check_cord)
    temp_node = Node(None, None, -1)
    for key, v in vec.items():
        right_way = True
        for p in path_tup:
            if v[p[0]] != p[1]:
                right_way = False
        if right_way:
            if labels[key] == 1:
                count_one += 1
            else:
                count_zero += 1
    if count_one == 0 and count_zero == 0:
        return None
    if count_one > count_zero:
        temp_node.label = 1
    else:
        temp_node.label = 0

    if count_one > count_zero:
        temp_node.success_count = count_one
    else:
        temp_node.success_count = count_zero

    return temp_node


def calculate_err_brute_force(root, vec, labels, path_tup):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        count_right = 0
        for key, v in vec.items():
            right_way = True
            for p in path_tup:
                if v[p[0]] != p[1]:
                    right_way = False
            if right_way:
                if labels[key] == root.label:
                    count_right += 1
        return count_right

    path_tup_1 = path_tup.copy()
    path_tup_1.append((root.cord, 0))
    path_tup_2 = path_tup.copy()
    path_tup_2.append((root.cord, 1))
    success_left = calculate_err_brute_force(root.left, vec, labels, path_tup_1)
    success_right = calculate_err_brute_force(root.right, vec, labels, path_tup_2)
    return success_left + success_right
