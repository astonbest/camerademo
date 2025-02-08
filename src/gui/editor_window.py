"""
图像编辑器窗口模块
提供图像编辑功能，包括旋转、亮度调节和AI文字添加
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QInputDialog, QSlider, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QPainter, QFont, QImage
from PyQt5.QtCore import Qt
from datetime import datetime
import cv2
import numpy as np
from src.ai.text_generator import TextGenerator
from typing import Optional

class EditorWindow(QMainWindow):
    """图像编辑器窗口类"""
    
    def __init__(self, image: np.ndarray):
        """
        初始化编辑器窗口
        
        Args:
            image (np.ndarray): 要编辑的图像
        """
        super().__init__()
        self.image = image
        self.edited_image = image.copy()
        self.setWindowTitle("照片编辑")
        self.text_generator = TextGenerator()  # AI文字生成器
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 图片显示
        self.image_label = QLabel()
        self.update_image_display()
        layout.addWidget(self.image_label)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.ai_text_btn = QPushButton("AI添加文字")
        self.save_btn = QPushButton("保存")
        self.cancel_btn = QPushButton("取消")
        
        toolbar.addWidget(self.ai_text_btn)
        toolbar.addWidget(self.save_btn)
        toolbar.addWidget(self.cancel_btn)
        
        # 添加更多编辑工具按钮
        self.rotate_left_btn = QPushButton("向左旋转")
        self.rotate_right_btn = QPushButton("向右旋转")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        
        toolbar.addWidget(self.rotate_left_btn)
        toolbar.addWidget(self.rotate_right_btn)
        toolbar.addWidget(QLabel("亮度:"))
        toolbar.addWidget(self.brightness_slider)
        
        # 添加AI设置按钮
        self.ai_settings_btn = QPushButton("AI设置")
        toolbar.addWidget(self.ai_settings_btn)
        self.ai_settings_btn.clicked.connect(self.show_ai_settings)
        
        layout.addLayout(toolbar)
        
        # 连接信号
        self.ai_text_btn.clicked.connect(self.add_ai_text)
        self.save_btn.clicked.connect(self.save_image)
        self.cancel_btn.clicked.connect(self.close)
        
        # 连接新增信号
        self.rotate_left_btn.clicked.connect(lambda: self.rotate_image(-90))
        self.rotate_right_btn.clicked.connect(lambda: self.rotate_image(90))
        self.brightness_slider.valueChanged.connect(self.adjust_brightness)
        
    def update_image_display(self):
        height, width = self.edited_image.shape[:2]
        bytes_per_line = 3 * width
        rgb_image = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2RGB)
        q_img = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap.scaled(
            800, 600, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        ))
        
    def rotate_image(self, angle):
        """旋转图像"""
        height, width = self.edited_image.shape[:2]
        center = (width//2, height//2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.edited_image = cv2.warpAffine(self.edited_image, rotation_matrix, (width, height))
        self.update_image_display()
        
    def adjust_brightness(self, value):
        """调整亮度"""
        img = self.image.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # 调整亮度值
        v = cv2.add(v, value)
        v[v > 255] = 255
        v[v < 0] = 0
        
        final_hsv = cv2.merge((h, s, v))
        self.edited_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        self.update_image_display()

    def add_ai_text(self):
        """使用AI生成并添加文字"""
        try:
            # 调用AI生成文字
            ai_text = self.text_generator.generate_text(self.image)
            
            text, ok = QInputDialog.getText(
                self, 
                "AI文字建议", 
                "AI生成的文字建议:\n" + ai_text + "\n\n请编辑或确认:",
                text=ai_text
            )
            
            if ok and text:
                img = self.edited_image.copy()
                # 自动计算文字位置和大小
                height, width = img.shape[:2]
                font_scale = min(width, height) / 500.0  # 根据图像大小调整字体
                thickness = max(1, int(font_scale * 2))
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                # 获取文字大小
                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                
                # 计算文字位置(居中)
                text_x = (width - text_size[0]) // 2
                text_y = height - 50  # 底部位置
                
                # 添加文字阴影效果
                cv2.putText(img, text, (text_x+2, text_y+2), font, font_scale, (0,0,0), thickness)
                cv2.putText(img, text, (text_x, text_y), font, font_scale, (255,255,255), thickness)
                
                self.edited_image = img
                self.update_image_display()
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"AI文字生成失败: {str(e)}")
    
    def save_image(self):
        """保存图片"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            "Images (*.jpg *.png)"
        )
        
        if file_name:
            cv2.imwrite(file_name, self.edited_image)
            self.close()
    
    def show_ai_settings(self):
        """显示AI设置对话框"""
        from .ai_settings_dialog import AISettingsDialog
        dialog = AISettingsDialog(self)
        dialog.exec_()