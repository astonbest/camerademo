from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QToolBar, QSizePolicy
from PyQt5.QtCore import Qt
from src.gui.preview_widget import PreviewWidget
from src.gui.settings_dialog import SettingsDialog
from src.gui.editor_window import EditorWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("相机应用")
        self.setup_ui()

    def setup_ui(self):
        self.resize(800, 600)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # 预览窗口
        self.preview = PreviewWidget()
        self.layout.addWidget(self.preview)
        
        # 设置预览窗口的尺寸策略
        self.preview.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        
        # 工具栏
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        
        # 添加按钮
        self.capture_btn = QPushButton("拍照")
        self.settings_btn = QPushButton("设置")
        self.toolbar.addWidget(self.capture_btn)
        self.toolbar.addWidget(self.settings_btn)
        
        # 连接信号
        self.capture_btn.clicked.connect(self.on_capture)
        self.settings_btn.clicked.connect(self.show_settings)
        
        # 允许窗口调整大小
        self.setMinimumSize(640, 480)
        self.resize(800, 600)
        
    def on_capture(self):
        image = self.preview.capture_photo()
        if image is not None:
            self.editor = EditorWindow(image)
            self.editor.show()
            
    def show_settings(self):
        dialog = SettingsDialog(self.preview.camera_manager)
        dialog.exec_()