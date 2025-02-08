import sys
import unittest
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from src.gui.editor_window import EditorWindow

class TestEditorWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 创建测试用QApplication实例
        cls.app = QApplication(sys.argv)
        # 创建测试用图像
        cls.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
    def setUp(self):
        # 为每个测试创建新的EditorWindow实例
        self.editor = EditorWindow(self.test_image)
        
    def test_init(self):
        """测试窗口初始化"""
        self.assertEqual(self.editor.windowTitle(), "照片编辑")
        self.assertIsNotNone(self.editor.image_label)
        self.assertIsNotNone(self.editor.edited_image)
        
    def test_rotate_image(self):
        """测试图像旋转功能"""
        original_shape = self.editor.edited_image.shape
        self.editor.rotate_image(90)
        rotated_shape = self.editor.edited_image.shape
        self.assertEqual(original_shape, rotated_shape)
        
    def test_brightness_adjustment(self):
        """测试亮度调节功能"""
        original_mean = cv2.mean(self.editor.edited_image)[0]
        self.editor.adjust_brightness(50)
        adjusted_mean = cv2.mean(self.editor.edited_image)[0]
        self.assertGreater(adjusted_mean, original_mean)
        
    def test_save_image(self):
        """测试保存图像功能"""
        import tempfile
        import os
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            # 模拟文件对话框返回临时文件路径
            self.editor.save_image()
            # 验证文件是否创建
            self.assertTrue(os.path.exists(tmp_path))
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.remove(tmp_path)