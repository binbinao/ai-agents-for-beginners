# QWEN.md - AI Agents for Beginners Course Context

## Project Overview

This is the "AI Agents for Beginners" educational course repository, created by Microsoft. It's a comprehensive learning resource that teaches everything needed to build AI Agents through 15+ structured lessons with hands-on code examples.

**Key Technologies:**
- Python 3.12+
- Jupyter Notebooks for interactive learning
- AI Frameworks: Semantic Kernel, AutoGen, Microsoft Agent Framework (MAF)
- Azure AI Services: Azure AI Foundry, Azure AI Agent Service
- GitHub Models Marketplace (free tier available)

**Course Structure:**
- Sequential lessons numbered 00-15+ in directories
- Each lesson contains: README documentation, code samples (Jupyter notebooks), and images
- Multi-language support via automated translation system
- Multiple framework implementations per lesson (Semantic Kernel, AutoGen, Azure AI Agent Service)

## Key Directories and Files

### Root Directory Structure
```
├── 00-course-setup/          # Initial setup instructions
├── 01-intro-to-ai-agents/    # Introduction to AI agents concepts
├── 02-explore-agentic-frameworks/  # Framework exploration
├── 03-agentic-design-patterns/     # Design patterns overview
├── 04-tool-use/              # Tool usage patterns
├── 05-agentic-rag/           # Retrieval-augmented generation
├── 06-building-trustworthy-agents/ # Trustworthy agent design
├── ...                       # Additional specialized lessons
├── 15-browser-use/           # Browser automation agents
├── .devcontainer/            # VS Code development container
├── .github/                  # GitHub Actions workflows
├── code_samples/             # Jupyter notebooks with examples
├── images/                   # Original English content images
├── translations/             # Multi-language content directories
└── ...                       # Configuration files
```

### Lesson Directory Structure
Each lesson follows a consistent pattern:
```
<lesson-number>-<lesson-name>/
├── README.md                     # Lesson documentation with objectives
├── code_samples/                 # Interactive examples
│   ├── <number>-semantic-kernel.ipynb
│   ├── <number>-autogen.ipynb
│   ├── <number>-python-agent-framework.ipynb
│   └── <number>-azureaiagent.ipynb
└── images/                       # Lesson-specific images
```

## Setup and Running Instructions

### Prerequisites
- Python 3.12 or higher
- GitHub account (for GitHub Models - free tier)
- Azure subscription (optional, for Azure AI services)

### Initial Setup
```bash
# 1. Clone or fork the repository:
gh repo fork microsoft/ai-agents-for-beginners --clone
# OR
git clone https://github.com/microsoft/ai-agents-for-beginners.git
cd ai-agents-for-beginners

# 2. Create and activate Python virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies:
pip install -r requirements.txt

# 4. Set up environment variables:
cp .env.example .env
# Edit .env with your API keys and endpoints
```

### Required Environment Variables

For **GitHub Models (Free)**:
- `GITHUB_TOKEN` - Personal access token from GitHub with models access

For **Azure AI Services** (optional):
- `PROJECT_ENDPOINT` - Azure AI Foundry project endpoint
- `AZURE_OPENAI_API_KEY` - Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint URL
- `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` - Deployment name for chat model
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME` - Deployment name for embeddings
- Additional Azure configuration as shown in `.env.example`

### Running Jupyter Notebooks

Each lesson contains multiple Jupyter notebooks for different frameworks:

```bash
# 1. Start Jupyter:
jupyter notebook

# 2. Navigate to a lesson directory (e.g., 01-intro-to-ai-agents/code_samples/)

# 3. Open and run notebooks:
# - *-semantic-kernel.ipynb - Using Semantic Kernel framework
# - *-autogen.ipynb - Using AutoGen framework  
# - *-python-agent-framework.ipynb - Using Microsoft Agent Framework (Python)
# - *-dotnet-agent-framework.ipynb - Using Microsoft Agent Framework (.NET)
# - *-azureaiagent.ipynb - Using Azure AI Agent Service
```

## Framework Options

The course supports multiple AI agent frameworks:

**Semantic Kernel + GitHub Models:**
- Free tier available with GitHub account
- Good for learning and experimentation
- File pattern: `*-semantic-kernel*.ipynb`

**AutoGen + GitHub Models:**
- Free tier available with GitHub account
- Multi-agent orchestration capabilities
- File pattern: `*-autogen.ipynb`

**Microsoft Agent Framework (MAF):**
- Latest framework from Microsoft
- Available in Python and .NET
- File pattern: `*-agent-framework.ipynb`

**Azure AI Agent Service:**
- Requires Azure subscription
- Production-ready features
- File pattern: `*-azureaiagent.ipynb`

## Development Conventions

### Python Conventions
- **Python Version**: 3.12+
- **Code Style**: Follow standard Python PEP 8 conventions
- **Notebooks**: Use clear markdown cells to explain concepts
- **Imports**: Group by standard library, third-party, local imports

### Jupyter Notebook Conventions
- Include descriptive markdown cells before code cells
- Add output examples in notebooks for reference
- Use clear variable names that match lesson concepts
- Keep notebook execution order linear (cell 1 → 2 → 3...)

### Multi-Language Support
- 50+ languages supported through automated translation
- Translations in `/translations/<lang-code>/` directories
- GitHub Actions workflow handles translation updates
- Source files are in English at repository root

## Key Dependencies (from requirements.txt)

- `autogen-agentchat`, `autogen-core`, `autogen-ext` - AutoGen framework
- `semantic-kernel` - Semantic Kernel framework  
- `agent-framework` - Microsoft Agent Framework
- `azure-ai-inference`, `azure-ai-projects` - Azure AI services
- `azure-search-documents` - Azure AI Search integration
- `chromadb` - Vector database for RAG examples
- `chainlit` - Chat UI framework
- `browser_use` - Browser automation for agents
- `mcp[cli]` - Model Context Protocol support
- `mem0ai` - Memory management for agents
- `openai`, `httpx`, `ipykernel`, `pillow`, `python-dotenv`, `pandas`, `uvicorn`, `nest-asyncio`

## Troubleshooting and Gotchas

1. **Python version mismatch**: Ensure Python 3.12+ is used; some packages may not work with older versions
2. **Environment variables**: Always create `.env` from `.env.example`; don't commit `.env` file (it's in `.gitignore`)
3. **Package conflicts**: Use a fresh virtual environment; install from `requirements.txt` rather than individual packages
4. **Azure services**: Azure AI services require active subscription; some features are region-specific
5. **Free tier limitations**: GitHub Models have free tier limitations

## Learning Path

Recommended progression through lessons:
1. **00-course-setup** - Start here for environment setup
2. **01-intro-to-ai-agents** - Understand AI agent fundamentals
3. **02-explore-agentic-frameworks** - Learn about different frameworks
4. **03-agentic-design-patterns** - Core design patterns
5. Continue through numbered lessons sequentially to lesson 15+

## Support and Resources

- Join the [Azure AI Foundry Community Discord](https://aka.ms/ai-agents/discord) for help and community
- Check the main [README.md](./README.md) for course overview
- Refer to [Course Setup](./00-course-setup/README.md) for detailed setup instructions
- See [GitHub Issues](https://github.com/microsoft/ai-agents-for-beginners/issues) for current needs

## Specialized Topics Covered

The course covers advanced AI agent concepts including:
- Tool usage design patterns
- Agentic RAG (Retrieval-Augmented Generation)
- Building trustworthy agents
- Planning design patterns
- Multi-agent systems
- Metacognition patterns
- Production deployment considerations
- Agentic protocols (MCP, A2A, NLWeb)
- Context engineering for agents
- Agent memory management
- Microsoft Agent Framework exploration
- Computer use agents