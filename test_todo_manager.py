import unittest
import os
import json
import subprocess

class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.todo_file = "test_todo_list.json"
        if os.path.exists(self.todo_file):
            os.remove(self.todo_file)

    def tearDown(self):
        if os.path.exists(self.todo_file):
            os.remove(self.todo_file)

    def run_command(self, args):
        result = subprocess.run(
            ["python3", "todo_manager.py", "--file", self.todo_file] + args,
            capture_output=True,
            text=True
        )
        return result

    def test_set_tasks(self):
        tasks = ["Update Core Auth Hook", "Refactor Login Components", "Update Dashboard Components", "Update API Integration", "Test Auth Flow"]
        result = self.run_command(["set_tasks", "--tasks"] + tasks)

        self.assertEqual(result.returncode, 0)
        self.assertIn("Tasks set", result.stdout)

        with open(self.todo_file, "r") as f:
            data = json.load(f)
            self.assertEqual(len(data["tasks"]), 5)
            self.assertEqual(data["tasks"][0]["name"], "Update Core Auth Hook")
            self.assertEqual(data["tasks"][0]["status"], "in-progress")
            self.assertEqual(data["tasks"][1]["status"], "todo")
            self.assertEqual(data["current_task"], "Update Core Auth Hook")

    def test_move_to_task(self):
        tasks = ["Task 1", "Task 2", "Task 3"]
        self.run_command(["set_tasks", "--tasks"] + tasks)

        result = self.run_command(["move_to_task", "--moveToTask", "Task 2"])

        self.assertEqual(result.returncode, 0)
        self.assertIn("Moved to task: Task 2", result.stdout)

        with open(self.todo_file, "r") as f:
            data = json.load(f)
            self.assertEqual(data["tasks"][0]["status"], "done")
            self.assertEqual(data["tasks"][1]["status"], "in-progress")
            self.assertEqual(data["current_task"], "Task 2")

    def test_auth_context_refactoring_scenario(self):
        # Scenario from the prompt
        tasks = [
            "Update Core Auth Hook",
            "Refactor Login Components",
            "Update Dashboard Components",
            "Update API Integration",
            "Test Auth Flow"
        ]

        # 1. Agent calls Todo Manager to create a systematic refactoring plan
        self.run_command(["set_tasks", "--tasks"] + tasks)

        with open(self.todo_file, "r") as f:
            data = json.load(f)
            self.assertEqual(data["current_task"], "Update Core Auth Hook")

        # Simulate moving through tasks
        self.run_command(["move_to_task", "--moveToTask", "Refactor Login Components"])
        with open(self.todo_file, "r") as f:
            data = json.load(f)
            self.assertEqual(data["tasks"][0]["status"], "done")
            self.assertEqual(data["current_task"], "Refactor Login Components")

        # Mark all done
        self.run_command(["mark_all_done"])
        with open(self.todo_file, "r") as f:
            data = json.load(f)
            self.assertTrue(all(t["status"] == "done" for t in data["tasks"]))
            self.assertIsNone(data["current_task"])

if __name__ == "__main__":
    unittest.main()
