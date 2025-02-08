"""
配置管理模块
处理应用程序的配置信息
"""

from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        "camera": {
            "device_id": 0,
            "resolution": (640, 480),
            "fps": 30
        },
        "ai": {
            "endpoint": "https://api.openai.com/v1",
            "model": "gpt-4-vision-preview"
        },
        "save_path": str(Path.home() / "Pictures" / "camera-app")
    }
    
    def __init__(self):
        self.config_file = Path.home() / ".camera-app" / "config.json"
        self.config = self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            return self.DEFAULT_CONFIG.copy()
            
    def save_config(self):
        """保存配置到文件"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")