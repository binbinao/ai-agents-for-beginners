# 使用自定义模型 (腾讯云/Deepseek) 运行 AI Agents 课程

本指南说明如何在没有 OpenAI 访问权限的情况下，使用腾讯云知识引擎或 Deepseek 模型运行 AI Agents for Beginners 课程。

## 配置步骤

### 1. 编辑 .env 文件

使用您的实际 API 凭据更新 `.env` 文件：

```env
# 对于腾讯云
OPENAI_API_KEY="your_tencent_cloud_api_key_here"
OPENAI_ENDPOINT="https://hunyuan.tencentcloudapi.com/v1"  # 替换为您的实际端点
OPENAI_CHAT_MODEL_ID="hunyuan-pro"  # 或其他腾讯云模型

# 对于 Deepseek
# OPENAI_API_KEY="your_deepseek_api_key_here"
# OPENAI_ENDPOINT="https://api.deepseek.com/v1"  # Deepseek 端点
# OPENAI_CHAT_MODEL_ID="deepseek-chat"  # 或 "deepseek-coder"
```

### 2. 安装依赖

确保安装了所有必需的包：

```bash
pip install -r requirements.txt
```

### 3. 测试连接

运行连接测试脚本以验证配置：

```bash
python test_connection.py
```

### 4. 运行更新的笔记本

本项目包含为腾讯云和 Deepseek 优化的笔记本文件：

- `01-intro-to-ai-agents/code_samples/01-python-agent-framework-custom.ipynb` - Microsoft Agent Framework 示例
- `01-intro-to-ai-agents/code_samples/01-semantic-kernel-custom.ipynb` - Semantic Kernel 示例  
- `02-explore-agentic-frameworks/code_samples/02-autogen-custom.ipynb` - AutoGen 示例

## 使用说明

1. **修改 .env 文件**：将占位符替换为您的实际 API 凭据
2. **运行测试**：使用 `test_connection.py` 验证连接
3. **选择笔记本**：使用后缀为 `-custom.ipynb` 的笔记本文件
4. **运行代码**：按顺序执行笔记本中的单元格

## 自定义模型适配器

`model_adapter.py` 文件包含以下功能：

- `CustomModelAdapter` - 用于连接自定义模型的主适配器
- `get_openai_client()` - 为 Microsoft Agent Framework 提供配置
- `get_semantic_kernel_config()` - 为 Semantic Kernel 提供配置
- `get_autogen_config()` - 为 AutoGen 提供配置

## 注意事项

- 确保您的 API 提供商支持 OpenAI 兼容格式
- 某些模型可能不支持所有功能（如函数调用或视觉能力）
- 请检查您的 API 使用限制和成本
- 如果遇到连接问题，请检查您的 API 密钥和端点是否正确

## 故障排除

如果笔记本无法正常工作：

1. 确认 `.env` 文件中的凭据是否正确
2. 运行 `test_connection.py` 检查基本连接
3. 检查您的 API 端点是否支持所需的功能（如函数调用）
4. 确认您的 API 密钥有足够的权限

完成这些配置后，您就可以使用腾讯云或 Deepseek 模型继续学习 AI Agents 课程了！