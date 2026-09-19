import os

from setuptools import setup, find_packages

setup(
    name="model_adapter",
    version="1.0.0",
    description="Model Adapter for Tencent Cloud and Deepseek API - Compatible with OpenAI format",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="AI Agents for Beginners",
    author_email="",
    url="https://github.com/microsoft/ai-agents-for-beginners",
    packages=find_packages(),
    py_modules=["model_adapter"],
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    keywords="ai, agents, openai, tencent, deepseek, adapter",
)