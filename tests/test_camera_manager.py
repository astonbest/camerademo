import unittest
import cv2
import numpy as np
from PyQt5.QtCore import QThread
from src.camera.camera_manager import CameraManager

class TestCameraManager(unittest.TestCase):
    def setUp(self):
        self.camera_manager = CameraManager()
        
    def test_init(self):
        """测试初始化"""
        self.assertFalse(self.camera_manager.running)
        self.assertIsNone(self.camera_manager.camera)
        self.assertEqual(self.camera_manager.camera_id, 0)
        
    def test_capture_photo(self):
        """测试拍照功能"""
        # 启动相机
        self.camera_manager.start()
        QThread.msleep(1000)  # 等待相机初始化
        
        # 测试拍照
        photo = self.camera_manager.capture_photo()
        self.assertIsNotNone(photo)
        self.assertEqual(len(photo.shape), 3)  # 确保是彩色图像
        
        # 清理
        self.camera_manager.stop()
        
    def tearDown(self):
        """测试清理"""
        if self.camera_manager.running:
            self.camera_manager.stop()