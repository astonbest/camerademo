from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import QSettings

class AISettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings('CameraApp', 'AISettings')
        self.setWindowTitle("AI服务配置")
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # API密钥设置
        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel("API密钥:"))
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        api_key_layout.addWidget(self.api_key_edit)
        layout.addLayout(api_key_layout)
        
        # API端点设置
        endpoint_layout = QHBoxLayout()
        endpoint_layout.addWidget(QLabel("API端点:"))
        self.endpoint_edit = QLineEdit()
        endpoint_layout.addWidget(self.endpoint_edit)
        layout.addLayout(endpoint_layout)
        
        # 模型选择
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("AI模型:"))
        self.model_edit = QLineEdit()
        model_layout.addWidget(self.model_edit)
        layout.addLayout(model_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("取消")
        test_btn = QPushButton("测试连接")
        
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        test_btn.clicked.connect(self.test_connection)
        
        button_layout.addWidget(test_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
    def load_settings(self):
        """从QSettings加载保存的设置"""
        self.api_key_edit.setText(self.settings.value('api_key', ''))
        self.endpoint_edit.setText(self.settings.value('endpoint', 'https://api.openai.com/v1'))
        self.model_edit.setText(self.settings.value('model', 'gpt-4-vision-preview'))
        
    def save_settings(self):
        """保存设置到QSettings"""
        self.settings.setValue('api_key', self.api_key_edit.text())
        self.settings.setValue('endpoint', self.endpoint_edit.text())
        self.settings.setValue('model', self.model_edit.text())
        self.accept()
        
    def test_connection(self):
        """测试API连接"""
        try:
            # 创建临时TextGenerator实例进行测试
            from ai.text_generator import TextGenerator
            generator = TextGenerator(
                api_key=self.api_key_edit.text(),
                endpoint=self.endpoint_edit.text(),
                model=self.model_edit.text()
            )
            if generator.test_connection():
                QMessageBox.information(self, "成功", "API连接测试成功！")
            else:
                QMessageBox.warning(self, "失败", "API连接测试失败，请检查配置。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"连接测试出错：{str(e)}")