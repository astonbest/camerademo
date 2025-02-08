#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
相机应用程序入口模块
提供主窗口的初始化和应用程序的启动

Author: Your Name
Date: 2024-02-07
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow  # 修改导入路径

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    主程序入口函数
    初始化QApplication并创建主窗口
    
    Returns:
        int: 程序退出码
    """
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        return app.exec_()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())