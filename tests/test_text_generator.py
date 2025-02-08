import unittest
import numpy as np
from unittest.mock import patch
from src.ai.text_generator import TextGenerator

class TestTextGenerator(unittest.TestCase):
    def setUp(self):
        self.text_generator = TextGenerator()
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
    @patch('requests.post')
    def test_generate_text(self, mock_post):
        """测试AI文本生成"""
        # 模拟API响应
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'choices': [{'message': {'content': '测试文本'}}]
        }
        
        result = self.text_generator.generate_text(self.test_image)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        
    @patch('requests.get')
    def test_connection(self, mock_get):
        """测试API连接"""
        mock_get.return_value.status_code = 200
        self.assertTrue(self.text_generator.test_connection())
        
        mock_get.return_value.status_code = 401
        self.assertFalse(self.text_generator.test_connection())