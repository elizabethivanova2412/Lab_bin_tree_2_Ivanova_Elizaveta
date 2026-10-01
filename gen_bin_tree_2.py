"""
Модуль для генерации бинарного дерева в виде словаря (итеративно).

Вариант: root = 6; height = 5
    left_leaf  = (root * 2) - 2
    right_leaf = root + 4

Каждый узел — словарь {"значение": [левый, правый]}. Лист — {"значение": []}.
Построение без рекурсии: используется стек задач.
"""

from typing import Callable, Dict, List, Tuple, Union

TreeNode = Dict[str, List[Union["TreeNode", list]]]


def left_branch(root: int) -> int:
    """Левый потомок: (root * 2) - 2."""
    return (root * 2) - 2


def right_branch(root: int) -> int:
    """Правый потомок: root + 4."""
    return root + 4


def _clean(node) -> None:
    """Заменить оставшиеся None на [] (лист без потомков)."""
    stack = [node]
    while stack:
        cur = stack.pop()
        if isinstance(cur, list):
            for item in cur:
                if isinstance(item, (dict, list)):
                    stack.append(item)
        elif isinstance(cur, dict):
            value = next(iter(cur))
            for i, child in enumerate(cur[value]):
                if child is None:
                    cur[value][i] = []
                else:
                    stack.append(child)


def gen_bin_tree(
    height: int = 5,
    root: int = 6,
    l_b: Callable[[int], int] = left_branch,
    r_b: Callable[[int], int] = right_branch,
) -> TreeNode:
    """
    Итеративно построить бинарное дерево и вернуть его в виде словаря.

    :param height: высота дерева (неотрицательное целое). По умолчанию 5.
    :param root: значение корневого узла. По умолчанию 6.
    :param l_b: функция вычисления значения левого потомка.
    :param r_b: функция вычисления значения правого потомка.
    :return: словарь, описывающий бинарное дерево.
    :raises ValueError: если height < 0.
    """
    if height < 0:
        raise ValueError("Высота дерева не может быть отрицательной")

    if height == 0:
        return {str(root): []}

    root_node: TreeNode = {str(root): [None, None]}

    stack: List[Tuple[int, int, list, int]] = [
        (l_b(root), 1, root_node[str(root)], 0),
        (r_b(root), 1, root_node[str(root)], 1),
    ]

    while stack:
        value, level, parent_children, side = stack.pop()

        if level < height:
            node: TreeNode = {str(value): [None, None]}
        else:
            node = {str(value): []}

        parent_children[side] = node

        if level < height:
            stack.append((l_b(value), level + 1, node[str(value)], 0))
            stack.append((r_b(value), level + 1, node[str(value)], 1))

    _clean(root_node)
    return root_node


if __name__ == "__main__":
    import pprint
    pprint.pprint(gen_bin_tree(2, 6), width=100)
