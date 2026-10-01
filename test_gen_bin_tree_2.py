"""
Тесты для функции gen_bin_tree (словарное представление дерева).
Запуск в Colab: unittest.main(argv=[''], verbosity=2, exit=False)
"""

import unittest

from gen_bin_tree import gen_bin_tree, left_branch, right_branch


class TestBranchFunctions(unittest.TestCase):
    """Проверка формул вычисления потомков."""

    def test_left_branch(self):
        self.assertEqual(left_branch(6), 10)
        self.assertEqual(left_branch(10), 18)
        self.assertEqual(left_branch(0), -2)

    def test_right_branch(self):
        self.assertEqual(right_branch(6), 10)
        self.assertEqual(right_branch(10), 14)
        self.assertEqual(right_branch(0), 4)


class TestGenBinTreeStructure(unittest.TestCase):
    """Проверка формы дерева для разных высот."""

    def test_height_zero(self):
        self.assertEqual(gen_bin_tree(0, 6), {"6": []})

    def test_height_one(self):
        expected = {"6": [{"10": []}, {"10": []}]}
        self.assertEqual(gen_bin_tree(1, 6), expected)

    def test_height_two(self):
        expected = {
            "6": [
                {"10": [{"18": []}, {"14": []}]},
                {"10": [{"18": []}, {"14": []}]},
            ]
        }
        self.assertEqual(gen_bin_tree(2, 6), expected)

    def test_root_value_is_custom(self):
        tree = gen_bin_tree(1, 100)
        self.assertIn("100", tree)
        self.assertEqual(list(tree.keys()), ["100"])

    def test_leaf_has_empty_list(self):
        tree = gen_bin_tree(1, 6)
        children = tree["6"]
        for leaf in children:
            value = next(iter(leaf))
            self.assertEqual(leaf[value], [])


class TestGenBinTreeDefaults(unittest.TestCase):
    """Проверка параметров по умолчанию."""

    def test_default_height_and_root(self):
        tree = gen_bin_tree()
        self.assertIn("6", tree)

    def test_default_height_number_of_nodes(self):
        tree = gen_bin_tree()
        self.assertEqual(self._count_nodes(tree), 63)

    def test_number_of_nodes_for_various_heights(self):
        for h in range(5):
            tree = gen_bin_tree(h, 6)
            self.assertEqual(self._count_nodes(tree), 2 ** (h + 1) - 1)

    @staticmethod
    def _count_nodes(tree: dict) -> int:
        if not tree:
            return 0
        value = next(iter(tree))
        children = tree[value]
        if not isinstance(children, list):
            return 1
        return 1 + sum(
            TestGenBinTreeDefaults._count_nodes(c) for c in children
        )


class TestGenBinTreeCustomBranches(unittest.TestCase):
    """Проверка подмены функций ветвления."""

    def test_custom_l_and_r(self):
        tree = gen_bin_tree(
            1, 5, l_b=lambda x: x + 1, r_b=lambda x: x ** 2
        )
        self.assertEqual(tree, {"5": [{"6": []}, {"25": []}]})

    def test_custom_left_only(self):
        tree = gen_bin_tree(1, 5, l_b=lambda x: x + 100)
        self.assertEqual(tree, {"5": [{"105": []}, {"9": []}]})

    def test_custom_right_only(self):
        tree = gen_bin_tree(1, 5, r_b=lambda x: x - 1)
        self.assertEqual(tree, {"5": [{"8": []}, {"4": []}]})


class TestGenBinTreeErrors(unittest.TestCase):
    """Проверка обработки некорректных параметров."""

    def test_negative_height_raises(self):
        with self.assertRaises(ValueError):
            gen_bin_tree(-1, 6)

    def test_large_negative_height_raises(self):
        with self.assertRaises(ValueError):
            gen_bin_tree(-100, 6)


class TestGenBinTreeVariant(unittest.TestCase):
    """Тесты варианта: root=6, height=5, L=(root*2)-2, R=root+4."""

    def test_left_formula_on_depth_one(self):
        tree = gen_bin_tree(1, 6)
        left_subtree = tree["6"][0]
        self.assertIn("10", left_subtree)

    def test_right_formula_on_depth_one(self):
        tree = gen_bin_tree(1, 6)
        right_subtree = tree["6"][1]
        self.assertIn("10", right_subtree)

    def test_second_level_values(self):
        tree = gen_bin_tree(2, 6)
        left = tree["6"][0]
        self.assertIn("18", left["10"][0])
        self.assertIn("14", left["10"][1])


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)
