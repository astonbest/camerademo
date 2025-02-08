from setuptools import setup, find_packages
import io

# 使用 UTF-8 编码读取 README
with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="camera-app",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A camera application with AI text generation capability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/camera-app",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.1",
        "numpy>=1.24.3",
        "PyQt5>=5.15.9",
        "requests>=2.31.0",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-qt>=4.2.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "camera-app=main:main",
        ],
    },
)