import unittest
from src.gui.editor_window import EditorWindow

class TestEditorWindow(unittest.TestCase):
    def setUp(self):
        self.editor = EditorWindow()

    def test_add_text(self):
        initial_text = "Hello"
        self.editor.add_text(initial_text)
        self.assertIn(initial_text, self.editor.image_text)

    def test_clear_text(self):
        self.editor.add_text("Sample text")
        self.editor.clear_text()
        self.assertEqual(self.editor.image_text, "")

    def test_apply_ai_text(self):
        self.editor.apply_ai_text("AI generated text")
        self.assertIn("AI generated text", self.editor.image_text)

if __name__ == '__main__':
    unittest.main()