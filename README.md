# 相机应用程序

基于 Python 的相机应用程序，支持实时预览和 AI 文字生成功能。

## 功能特点

- 实时相机预览
- 相机参数设置
- 图片拍摄和编辑
- AI辅助文字生成
- 图片保存功能

## 系统要求

- Python 3.8+
- OpenCV 4.8+
- PyQt5 5.15+
- 支持的操作系统：Windows/Linux/MacOS

## 安装

```bash
pip install -e ".[dev]"
```

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/camera-app.git
cd camera-app
```

2. 安装依赖项：

```bash
pip install -r requirements.txt
```

## 使用

```bash
camera-app
```

运行主程序：

```bash
python src/main.py
```

## 运行方式

1. 开发模式运行：
```bash
# 激活虚拟环境
.\venv\Scripts\activate

# 在项目根目录下执行
python -m src.main
```

2. 安装后运行：
```bash
camera-app
```

## 故障排除

如果遇到导入错误，请检查：
1. 是否已激活虚拟环境
2. 是否在项目根目录下运行
3. 是否已正确安装所有依赖

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。