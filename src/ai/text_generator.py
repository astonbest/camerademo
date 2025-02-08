# filepath: /e:/Projects/camerademo/camera-app/src/ai/text_generator.py
# -*- coding: utf-8 -*-
"""
AI文本生成器模块
负责处理图像到文本的转换
"""

import cv2
import numpy as np
from PIL import Image
import requests
from PyQt5.QtCore import QSettings

class TextGenerator:
    def __init__(self):
        self.api_key = None
        self.model = "gpt-4-vision-preview"
    
    def generate_text(self, image):
        """生成图像描述文本"""
        return "测试文本"