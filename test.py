"""Potion Workshop - 로직 단위 테스트.

pygame 을 전혀 import 하지 않으므로 그래픽 환경 없이도
빠르고 안전하게 게임 로직을 검증/디버깅할 수 있다.

    python test.py
"""

import unittest

import dialogue_engine as de
import game_logic as gl


class TestDialogueEngine(unittest.TestCase):
    def test_ease_in_out_cubic_bounds(self):
        self.assertEqual(de.ease_in_out_cubic(0), 0)
        self.assertEqual(de.ease_in_out_cubic(1), 1)
        self.assertAlmostEqual(de.ease_in_out_cubic(0.5), 0.5)

    def test_ease_in_out_cubic_clamps(self):
        self.assertEqual(de.ease_in_out_cubic(-1), 0)
        self.assertEqual(de.ease_in_out_cubic(2), 1)


class TestRecipes(unittest.TestCase):
    def test_all_four_potions_craftable(self):
        for recipe in gl.RECIPES:
            result = gl.get_potion_by_ingredients(recipe["ingredients"])
            self.assertEqual(result["potion_id"], recipe["potion_id"])

    def test_order_does_not_matter(self):
        a = gl.get_potion_by_ingredients(["red_mushroom", "yellow_petal"])
        b = gl.get_potion_by_ingredients(["yellow_petal", "red_mushroom"])
        self.assertEqual(a["potion_id"], "healing")
        self.assertEqual(b["potion_id"], "healing")

    def test_invalid_combo_is_failed(self):
        result = gl.get_potion_by_ingredients(["red_mushroom", "black_root"])
        self.assertEqual(result["potion_id"], "failed")
        self.assertEqual(result["ingredients"], ["red_mushroom", "black_root"])

    def test_recipes_use_known_ingredients(self):
        ids = {ing["id"] for ing in gl.INGREDIENTS}
        for recipe in gl.RECIPES:
            for ing_id in recipe["ingredients"]:
                self.assertIn(ing_id, ids)


class TestEvaluate(unittest.TestCase):
    def test_correct(self):
        correct, gold = gl.evaluate("healing", "healing")
        self.assertTrue(correct)
        self.assertEqual(gold, gl.REWARD_CORRECT)

    def test_wrong(self):
        correct, gold = gl.evaluate("sleep", "healing")
        self.assertFalse(correct)
        self.assertEqual(gold, gl.REWARD_WRONG)

    def test_failed_potion_never_correct(self):
        correct, gold = gl.evaluate("failed", "failed")
        self.assertFalse(correct)
        self.assertEqual(gold, gl.REWARD_WRONG)


class TestDayGeneration(unittest.TestCase):
    def test_customer_counts(self):
        rng = __import__("random").Random(1)
        self.assertEqual(len(gl.generate_day_customers(1, rng)), 3)
        self.assertEqual(len(gl.generate_day_customers(2, rng)), 4)
        self.assertEqual(len(gl.generate_day_customers(3, rng)), 5)
        self.assertEqual(len(gl.generate_day_customers(99, rng)), 5)

    def test_targets_within_available_potions(self):
        import random
        for day in (1, 2, 3, 4):
            rng = random.Random(day)
            available = set(gl.get_day_config(day)["potions"])
            for entry in gl.generate_day_customers(day, rng):
                self.assertIn(entry["target_potion"], available)

    def test_day1_tutorial_first_customers(self):
        import random
        customers = gl.generate_day_customers(1, random.Random(5))
        self.assertEqual(customers[0]["target_potion"], "healing")
        self.assertEqual(customers[0]["order_line"], gl.TUTORIAL_LINES["healing"])
        self.assertEqual(customers[1]["target_potion"], "strength")

    def test_every_order_line_belongs_to_target(self):
        import random
        for day in (2, 3, 4):
            rng = random.Random(day)
            for entry in gl.generate_day_customers(day, rng):
                target = entry["target_potion"]
                self.assertIn(entry["order_line"], gl.ORDER_LINES[target])


class TestBrewingFlow(unittest.TestCase):
    def setUp(self):
        self.gs = gl.GameState(seed=42)

    def test_add_ingredient_rules(self):
        self.assertTrue(self.gs.add_ingredient("red_mushroom"))
        # 중복 불가
        self.assertFalse(self.gs.add_ingredient("red_mushroom"))
        self.assertTrue(self.gs.add_ingredient("yellow_petal"))
        # 최대 2개
        self.assertFalse(self.gs.add_ingredient("star_dust"))
        self.assertEqual(len(self.gs.selected), 2)

    def test_unknown_ingredient_rejected(self):
        self.assertFalse(self.gs.add_ingredient("dragon_egg"))

    def test_clear(self):
        self.gs.add_ingredient("red_mushroom")
        self.gs.clear_ingredients()
        self.assertEqual(self.gs.selected, [])
        self.assertEqual(self.gs.phase, gl.PHASE_ORDER)

    def test_craft_requires_two(self):
        self.gs.add_ingredient("red_mushroom")
        self.assertFalse(self.gs.can_craft())
        self.assertFalse(self.gs.craft())
        self.gs.add_ingredient("yellow_petal")
        self.assertTrue(self.gs.craft())
        self.assertEqual(self.gs.phase, gl.PHASE_CRAFTED)
        self.assertEqual(self.gs.crafted_potion["potion_id"], "healing")

    def test_submit_requires_crafted(self):
        self.assertFalse(self.gs.submit())
        self.gs.add_ingredient("red_mushroom")
        self.gs.add_ingredient("yellow_petal")
        self.gs.craft()
        self.assertTrue(self.gs.submit())
        self.assertEqual(self.gs.phase, gl.PHASE_RESULT)
        self.assertIsNotNone(self.gs.last_result)


class TestFullDayProgression(unittest.TestCase):
    def _serve_correct(self, gs):
        target = gs.current_customer["target_potion"]
        recipe = gl.get_recipe(target)
        for ing in recipe["ingredients"]:
            gs.add_ingredient(ing)
        gs.craft()
        gs.submit()
        result = gs.last_result
        gs.next_customer()
        return result

    def test_perfect_day_advances(self):
        gs = gl.GameState(seed=7)
        self.assertEqual(gs.day, 1)
        for _ in range(gs.total_customers):
            res = self._serve_correct(gs)
            self.assertTrue(res["correct"])
        self.assertEqual(gs.phase, gl.PHASE_DAY_END)
        self.assertTrue(gs.day_success)
        gs.advance_day()
        self.assertEqual(gs.day, 2)
        self.assertEqual(gs.gold_today, 0)

    def test_failed_day_retries(self):
        gs = gl.GameState(seed=7)
        # 모든 손님에게 일부러 틀린(수상한) 포션 제출
        for _ in range(gs.total_customers):
            gs.add_ingredient("red_mushroom")
            gs.add_ingredient("black_root")  # 어떤 레시피도 아님
            gs.craft()
            self.assertEqual(gs.crafted_potion["potion_id"], "failed")
            gs.submit()
            gs.next_customer()
        self.assertEqual(gs.phase, gl.PHASE_DAY_END)
        self.assertFalse(gs.day_success)
        gs.advance_day()
        self.assertEqual(gs.day, 1)  # 같은 날 재도전

    def test_gold_accumulates_across_days(self):
        gs = gl.GameState(seed=3)
        for _ in range(gs.total_customers):
            self._serve_correct(gs)
        day1_gold = gs.gold
        gs.advance_day()
        for _ in range(gs.total_customers):
            self._serve_correct(gs)
        self.assertGreater(gs.gold, day1_gold)


if __name__ == "__main__":
    unittest.main(verbosity=2)
