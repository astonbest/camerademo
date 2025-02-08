from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
from camera.camera_manager import CameraManager
import cv2

class PreviewWidget(QWidget):
    def __init__(self, parent=None):
        super(PreviewWidget, self).__init__(parent)
        self.setWindowTitle("Camera Preview")
        self.layout = QVBoxLayout(self)
        
        # 创建预览标签
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.preview_label)
        
        # 设置最小尺寸
        self.setMinimumSize(320, 240)
        
        # 初始化相机管理器
        self.camera_manager = CameraManager()
        self.camera_manager.frame_ready.connect(self.update_frame)
        self.camera_manager.start()
        
    def update_frame(self, frame):
        self.display_frame(frame)
        
    def display_frame(self, frame):
        """显示帧图像"""
        if frame is None:
            return
            
        self.current_frame = frame
        height, width = frame.shape[:2]
        
        # 计算适应窗口的缩放尺寸
        widget_size = self.size()
        scale_w = widget_size.width() / width
        scale_h = widget_size.height() / height
        scale = min(scale_w, scale_h)
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # 转换图像格式并缩放
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img).scaled(
            new_width, new_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        self.preview_label.setPixmap(pixmap)
        
    def resizeEvent(self, event):
        """重写调整大小事件"""
        super().resizeEvent(event)
        self.update_frame_size()
        
    def update_frame_size(self):
        """更新帧显示尺寸"""
        if hasattr(self, 'current_frame'):
            self.display_frame(self.current_frame)
        
    def capture_photo(self):
        return self.camera_manager.capture_photo()
        
    def closeEvent(self, event):
        self.camera_manager.stop()
        event.accept()