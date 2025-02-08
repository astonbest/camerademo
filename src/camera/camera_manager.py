"""
相机管理模块
负责处理摄像头的初始化、图像捕获和参数设置
"""

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import time
from typing import Optional, Tuple

class CameraManager(QThread):
    """
    相机管理器类
    继承自QThread，提供异步相机操作
    """
    
    # 信号定义
    frame_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, camera_id=0):
        """初始化相机管理器"""
        super().__init__()
        self.running = False
        self.camera: Optional[cv2.VideoCapture] = None
        self.camera_id = camera_id
        self.frame_interval = 1/30  # 30 FPS
        self._current_resolution = (640, 480)
        
    @property
    def resolution(self) -> Tuple[int, int]:
        """获取当前分辨率"""
        return self._current_resolution
        
    @resolution.setter
    def resolution(self, value: Tuple[int, int]):
        """设置相机分辨率"""
        if self.camera:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, value[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, value[1])
            self._current_resolution = value
            
    def run(self):
        """运行摄像头捕获线程"""
        if not self.initialize_camera():
            return
            
        self.running = True
        while self.running:
            if self.camera and self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    self.frame_ready.emit(frame)
                else:
                    self.error_occurred.emit("读取摄像头帧失败")
                    break
            time.sleep(self.frame_interval)
            
    def stop(self):
        """停止相机捕获"""
        self.running = False
        if self.camera:
            self.camera.release()
            self.camera = None
            
    def capture_photo(self) -> Optional[np.ndarray]:
        """
        捕获单张照片
        
        Returns:
            Optional[np.ndarray]: 捕获的图像数据，如果失败则返回None
        """
        if not self.camera or not self.camera.isOpened():
            return None
            
        ret, frame = self.camera.read()
        return frame if ret else None
        
    def initialize_camera(self):
        """初始化摄像头并检查可用性"""
        try:
            if self.camera and self.camera.isOpened():
                self.camera.release()
                
            self.camera = cv2.VideoCapture(self.camera_id)
            if not self.camera.isOpened():
                self.error_occurred.emit("无法打开摄像头，请检查设备连接")
                return False
                
            # 尝试设置默认分辨率
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self._current_resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self._current_resolution[1])
            
            # 获取实际支持的分辨率
            actual_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self._current_resolution = (actual_width, actual_height)
            
            return True
        except Exception as e:
            self.error_occurred.emit(f"摄像头初始化失败: {str(e)}")
            return False
        
    def __del__(self):
        """析构函数，确保资源释放"""
        self.stop()