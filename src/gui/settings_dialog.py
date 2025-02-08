import cv2
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QSpinBox, QComboBox, QPushButton)
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, camera_manager):
        super().__init__()
        self.camera_manager = camera_manager
        self.setWindowTitle("相机设置")
        self.setup_ui()
        self.load_current_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 分辨率设置
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(QLabel("分辨率:"))
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])
        resolution_layout.addWidget(self.resolution_combo)
        layout.addLayout(resolution_layout)
        
        # 亮度设置
        brightness_layout = QHBoxLayout()
        brightness_layout.addWidget(QLabel("亮度:"))
        self.brightness_spin = QSpinBox()
        self.brightness_spin.setRange(0, 100)
        self.brightness_spin.setValue(50)
        brightness_layout.addWidget(self.brightness_spin)
        layout.addLayout(brightness_layout)
        
        # 对比度设置
        contrast_layout = QHBoxLayout()
        contrast_layout.addWidget(QLabel("对比度:"))
        self.contrast_spin = QSpinBox()
        self.contrast_spin.setRange(0, 100)
        self.contrast_spin.setValue(50)
        contrast_layout.addWidget(self.contrast_spin)
        layout.addLayout(contrast_layout)
        
        # 确定取消按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
    def load_current_settings(self):
        """加载当前相机设置"""
        try:
            cap = self.camera_manager.camera
            if cap and cap.isOpened():
                # 获取当前分辨率
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                current_resolution = f"{width}x{height}"
                index = self.resolution_combo.findText(current_resolution)
                if index >= 0:
                    self.resolution_combo.setCurrentIndex(index)
                
                # 获取当前亮度
                brightness = int(cap.get(cv2.CAP_PROP_BRIGHTNESS))
                self.brightness_spin.setValue(brightness)
                
                # 获取当前对比度
                contrast = int(cap.get(cv2.CAP_PROP_CONTRAST))
                self.contrast_spin.setValue(contrast)
        except Exception as e:
            print(f"加载相机设置失败: {str(e)}")
    
    def accept(self):
        """应用设置并关闭对话框"""
        try:
            cap = self.camera_manager.camera
            if not (cap and cap.isOpened()):
                raise Exception("摄像头未打开")
                
            # 获取当前实际分辨率
            current_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            current_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # 解析目标分辨率
            resolution = self.resolution_combo.currentText()
            width, height = map(int, resolution.split('x'))
            
            # 如果分辨率发生变化，需要重新初始化摄像头
            if width != current_width or height != current_height:
                # 先保存新的分辨率设置
                self.camera_manager._current_resolution = (width, height)
                # 重新初始化摄像头
                if not self.camera_manager.initialize_camera():
                    raise Exception("无法应用新的分辨率设置")
                
                # 通知主窗口更新预览尺寸
                if hasattr(self.parent(), 'preview'):
                    self.parent().preview.update_frame_size()
            
            # 设置其他参数
            brightness = self.brightness_spin.value()
            contrast = self.contrast_spin.value()
            
            if not cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness):
                print("警告：无法设置亮度")
            if not cap.set(cv2.CAP_PROP_CONTRAST, contrast):
                print("警告：无法设置对比度")
                
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "设置失败", str(e))
            return
            
        super().accept()