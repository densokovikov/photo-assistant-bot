import unittest

from export_data import assignment_rows


class AssignmentRowsTest(unittest.TestCase):
    def test_returns_one_complete_lesson_per_course_topic(self):
        lessons = assignment_rows()

        self.assertEqual(len(lessons), 34)
        self.assertEqual(lessons[0]["topic_index"], 0)
        self.assertTrue(lessons[0]["theory"])
        self.assertEqual(len(lessons[0]["practice"]), 3)
        self.assertEqual(len(lessons[0]["advice"]), 2)
        self.assertTrue(lessons[0]["result"])
        self.assertTrue(lessons[0]["source"])


if __name__ == "__main__":
    unittest.main()
