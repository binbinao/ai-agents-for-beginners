# AGENTS.md

Guidance for agents and humans working in this checkout. Upstream project: Microsoft
[ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners). This working copy
also carries a small **local customization layer** that lets the lessons run against
OpenAI-compatible endpoints (Tencent Cloud Hunyuan / Deepseek) instead of OpenAI or Azure.
See [§12](#12-本地化改造说明中文章节) for the Chinese notes on that layer.

## 1. What this repository is

An educational course: 16 lesson directories (`00`–`15`), each with a `README.md`, code samples,
and images. Lessons teach fundamentals, design patterns, frameworks, and production concerns for
AI agents. There is **no test suite** — the notebooks are the executable artifacts.

Supported stacks in the samples: Semantic Kernel, AutoGen, Microsoft Agent Framework (Python and
.NET), Azure AI Agent Service, plus MCP and A2A protocol samples.

## 2. Repository layout (verified against this checkout)

| Path | Contents |
| --- | --- |
| `00-course-setup/` | Setup guide + Azure Search docs/scripts; no `code_samples/` |
| `01-intro-to-ai-agents/` … `12-context-engineering/` | `code_samples/` + `images/` |
| `13-agent-memory/` | Single notebook at lesson root |
| `14-microsoft-agent-framework/` | `code-samples/` (**hyphen**, not underscore) + `images/` |
| `15-browser-use/` | Notebook at lesson root + `llms.txt` |
| `images/`, `translated_images/`, `translations/` | Course art and the auto-translation output (50+ languages) |
| `model_adapter.py`, `setup.py`, `test_connection.py` | Local customization layer |
| `CUSTOM_MODEL_INSTRUCTIONS.md` | User-facing Chinese guide for that layer |
| `slide-deck/` | Local slide-deck project (see §11) |

Sample file naming is **not uniform**. Real patterns found here:

- `<NN>-<framework>.ipynb` — `01-semantic-kernel.ipynb`, `04-autogen.ipynb`, `14-…` in most lessons;
  frameworks seen: `semantic-kernel`, `python-agent-framework`, `autogen`, `azureaiagent`.
- Variant suffixes: `-custom` (local model path), `-tool`, `-chromadb`, `-azuresearch`,
  `-azure-ai-agent`, `-python-aiagent-bookinghotel`.
- .NET samples are usually `<NN>-dotnet-agent-framework.cs` + a companion `.md`. Lesson 08's
  `code_samples/workflows-agent-framework/dotNET/` also ships `.ipynb` versions of each sample.
- Lesson 08 nests deeper and numbers with dots:
  `code_samples/workflows-agent-framework/{python,dotNET}/01.python-agent-framework-workflow-ghmodel-basic.ipynb`.
- Lesson 14 numbers by topic instead of framework, e.g. `14-human-loop.ipynb`, `14-middleware.ipynb`,
  plus a `hotel_booking_workflow_sample.py`.
- Lesson 15 relies on a separate `browser-use` install path; read its README first.

Do not assume a template from one lesson generalizes to the next — list the directory first.

## 3. Environment setup

Python **3.12+** is required. This checkout currently uses a `uv`-created `.venv` (Python 3.12.13).

```bash
python3 -m venv .venv            # or: uv venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env             # then fill in credentials
```

Known gaps in `requirements.txt` (checked, not folklore):

- **No version pins at all.** Every install floats to latest; expect breakage over time.
- `jupyter`, `notebook`, `nbconvert`, `nbformat`, `jupyterlab` are **absent**. `ipykernel` is present,
  so notebooks run from a Jupyter you already have, but `jupyter notebook` and `jupyter nbconvert`
  both exit `1` in this venv. Install what you need explicitly:
  `pip install jupyterlab nbconvert`.
- `setuptools` is **absent from a fresh `uv venv`**, yet `setup.py` needs it. Install it before
  `pip install -e .`.
- Packages that earlier revisions of this file claimed were dependencies — `chromadb`, `chainlit`,
  `browser_use`, `mem0ai` — are **not** in `requirements.txt`. Lesson notebooks pull their own extras.

## 4. Credentials and secrets

- `.env` is gitignored. **Never read, print, or commit it.** Use `.env.example` as the catalog.
- **Known leak in this repository's history:** `02-explore-agentic-frameworks/code_samples/02-autogen-custom.ipynb`
  (cell 2) contains a plaintext API key — endpoint `https://api.lkeap.cloud.tencent.com/v1`,
  model `deepseek-v3-0324` — introduced in commit `c0f4796b`. Treat that key as burned and rotate it
  at the provider. Leave the notebook untouched unless the task is specifically about it; do not
  rewrite git history to hide it.
- New samples must read credentials from the environment, never literals.

## 5. Environment variables

`.env.example` defines 19 names. Three groups matter:

| Group | Variables | Used by |
| --- | --- | --- |
| GitHub Models (free tier) | `GITHUB_TOKEN`, `GITHUB_ENDPOINT`, `GITHUB_MODEL_ID` | Framework notebooks |
| Local OpenAI-compatible | `OPENAI_API_KEY`, `OPENAI_ENDPOINT`, `OPENAI_CHAT_MODEL_ID` | `model_adapter.py`, `test_connection.py`, `*-custom.ipynb` |
| Azure AI | `PROJECT_ENDPOINT`, `AZURE_OPENAI_*`, `AZURE_SEARCH_*`, `AZURE_AI_AGENT_*`, `AZURE_SUBSCRIPTION_ID`, `GLOBAL_LLM_SERVICE` | Azure lessons |

`GLOBAL_LLM_SERVICE` is the Azure AI Services connection name and is documented in
`00-course-setup/README.md`. The `.env.example` catalog lists names for the whole course; a given
lesson may read only a few of them, so verify a variable's real consumer before "cleaning it up".

## 6. Running notebooks

```bash
source .venv/bin/activate
python -m ipykernel install --user --name ai-agents-for-beginners \
       --display-name "Python (ai-agents-for-beginners)"
jupyter notebook                     # needs `pip install notebook` or jupyterlab
```

- Most notebooks declare `kernelspec.name = "python3"`. 22 notebooks additionally carry a stale
  committed `display_name` such as `".venv (3.12.11)"` — cosmetic, but it means the committed
  metadata does not describe your interpreter. Prefer selecting the explicit
  **Python (ai-agents-for-beginners)** kernel, which pins `.venv/bin/python`.
- Launch Jupyter from the repository root so `python-dotenv` finds `.env`.
- Headless smoke test (after installing `nbconvert`):
  `jupyter nbconvert --to script <lesson>/code_samples/<notebook>.ipynb --stdout | python`

## 7. Local customization layer

`model_adapter.py` exposes:

- `CustomModelAdapter` — `sync_chat_completion()`, `await chat_completion()`, `test_connection()`;
  raises at construction when key/endpoint/model are missing.
- `create_default_adapter()`, `AsyncCustomModelAdapter` (async context manager).
- `get_openai_client()` (async), `get_sync_openai_client()`, `get_semantic_kernel_config()`,
  `get_autogen_config()`.

Rules that are easy to get wrong:

- `_resolve_config()` resolves `OPENAI_*` **or** `GITHUB_*`, using `or` fallbacks, so an empty
  `OPENAI_API_KEY=` correctly falls through to `GITHUB_TOKEN`. Note `test_connection.py` uses
  `os.getenv(a, os.getenv(b))` instead, which does *not* fall through on an empty value.
- `openai>=1.0` removed the v0 surface: use `client.chat.completions.create(...)`. The old
  `openai.chat.completions.acreate` raises `AttributeError`.
- Assigning `openai.api_key` / `openai.base_url` in `CustomModelAdapter.__init__` is **intentional
  process-global configuration**, not dead code: module-level `openai.chat.completions` accessors
  resolve to a shared *blocking* default client that honors those globals. Prefer the explicit
  clients for new code; see the docstrings before deleting either mechanism.
- `get_semantic_kernel_config()` returns `model_id`, while `get_autogen_config()` returns `model`
  and `base_url`. The different key names are deliberate — AutoGen's client expects its own.

```bash
pip install -e .                 # installs the adapter as a package; requires setuptools
python test_connection.py        # 4 checks; exits 1 if any of them fails
```

`CUSTOM_MODEL_INSTRUCTIONS.md` documents the same layer for end users in Chinese. The three
custom notebooks are `01-…/01-python-agent-framework-custom.ipynb`,
`01-…/01-semantic-kernel-custom.ipynb`, and `02-…/02-autogen-custom.ipynb`.

## 8. Verification without credentials

There is no test suite; verify what you can offline, then report what you could not check.

```bash
.venv/bin/python -c "import openai, semantic_kernel, agent_framework, autogen_agentchat; print('ok')"
.venv/bin/python setup.py --name --version          # model_adapter / 1.0.0
.venv/bin/python -m jupyter kernelspec list
.venv/bin/python test_connection.py                 # needs a live endpoint; exit code is the signal
```

To exercise the adapter without a real provider, point `OPENAI_ENDPOINT` at a local mock that speaks
`POST /v1/chat/completions` and returns a `chat.completion` object. That is enough to prove both the
sync and async paths end to end.

## 9. Common issues

| Symptom | Cause / fix |
| --- | --- |
| `ModuleNotFoundError: setuptools` on `pip install -e .` | Fresh `uv venv` ships without it — `pip install setuptools` |
| `jupyter notebook` / `nbconvert` exit `1` | Not in `requirements.txt` — install explicitly |
| Kernel "not found" warnings on open | Committed `display_name` (`.venv (3.12.11)`) is stale; select the registered kernel |
| `.venv/bin/python` missing or broken | A `uv` upgrade can leave dangling interpreter symlinks; recreate the venv |
| `model_adapter.egg-info/`, `build/`, `dist/` appear | Local packaging output; gitignored since this layer was added |
| Notebook CLI run fails on imports | Re-run `pip install -r requirements.txt` inside the activated venv |

Also gitignored and easy to mistake for content: `*-backup.ipynb`,
`02-explore-agentic-frameworks/code_samples/*.png`, `05-agentic-rag/code_samples/chroma_db/`.

## 10. Contributing

- Upstream is `microsoft/ai-agents-for-beginners`; `translations/` and `translated_images/` are
  generated by GitHub Actions — never hand-edit them.
- One logical change per commit, with a message that explains *why*. Run the affected notebook(s)
  end to end before proposing the change.
- Do not commit `.env`, virtual environments, `__pycache__/`, or packaging artifacts.
- PR titles here have used the forms `[Lesson-XX] …`, `[Fix] …`, `[Update] …`, `[Docs] …`.

## 11. Slide deck project (`slide-deck/`)

A local, non-upstream addition that renders one handwritten-style deck per lesson chapter.

- `slide-deck/_shared/DESIGN-SYSTEM.md` is the **single source of truth** for style. Every chapter's
  outline copies its `<STYLE_INSTRUCTIONS>` block verbatim, so changing style means changing that
  file and regenerating, never editing one chapter's prompts by hand.
- `slide-deck/_shared/build_prompts.py <chapter-dir>` assembles `prompts/NN-slide-*.md` from
  `outline.md` + the design system + the `baoyu-slide-deck` skill's base prompt. It backs up any
  file it overwrites.
- Never patch rendered text by drawing over a generated bitmap; fix the prompt and regenerate.

## 12. 本地化改造说明（中文章节）

这一节记录本 checkout 相对上游新增的东西，以及踩过的坑。上游内容请只看英文部分。

**目的**：在没有 OpenAI / Azure 访问权限的情况下，用腾讯云混元或 Deepseek 这类 OpenAI 兼容端点
把课程跑起来。

**新增文件**

| 文件 | 作用 |
| --- | --- |
| `model_adapter.py` | 统一适配器：同步 / 异步 chat completion、Semantic Kernel / AutoGen / MAF 三种配置出口 |
| `test_connection.py` | 四步连通性自检（基础连接 / 适配器 / 框架配置 / 异步），任一项失败即退出码 1 |
| `setup.py` | 把适配器装成包，便于 notebook `import model_adapter` |
| `CUSTOM_MODEL_INSTRUCTIONS.md` | 面向使用者的中文配置指南 |
| `*-custom.ipynb`（3 个） | 01 章的 MAF / Semantic Kernel 与 02 章的 AutoGen 定制版 |
| `slide-deck/` | 按章生成手写风幻灯片（见第 11 节） |

**已修复的问题（各一个 commit，均有离线验证）**

1. `setup.py` 缺少 `import os`，第 7 行 `os.path.exists` 直接 `NameError`，导致 `pip install -e .`
   必然失败；顺手删掉误列的 `asyncio`（标准库，不是 PyPI 依赖）。
2. `model_adapter.py` 用了 openai v0 的 `openai.chat.completions.acreate`，在 openai 1.x/3.x 上抛
   `AttributeError`；改为 `self.async_client.chat.completions.create`，并补上
   `_resolve_config()` 让空值能正确回退到 `GITHUB_*`。
3. `test_connection.py` 无论成败都退出 0，CI 里等于没有信号；现在按结果给退出码，且框架配置检查
   不再无条件返回 `True`。
4. 忽略本地打包产物（`*.egg-info/`、`build/`、`dist/`），并把已经误入库的
   `model_adapter.egg-info/` 从索引里移出。
5. 删除根目录那个只在包上下文里才成立的 `__init__.py`（`from .model_adapter import ...` 无人引用）。

**必须记住的两件事**

- `02-explore-agentic-frameworks/code_samples/02-autogen-custom.ipynb` 第 2 个单元格里有一把明文
  密钥（端点是腾讯云知识引擎，模型 `deepseek-v3-0324`，随 commit `c0f4796b` 入库）。**该密钥应视为
  已泄露，请在腾讯云控制台作废重建**；本仓库不改写历史，也不在无关改动里动这个 notebook。
- `requirements.txt` 没有任何版本钉，且不含 `jupyter` / `notebook` / `nbconvert` / `jupyterlab`；
  新环境还要单独装 `setuptools` 才能 `pip install -e .`。

**本地环境现状**：`.venv` 由 `uv` 重建（Python 3.12.13），旧的坏环境已在校验通过后删除；已注册
用户级 kernel `Python (ai-agents-for-beginners)`。默认从仓库根目录启动 Jupyter，确保 `.env` 能被
读到。若再次遇到 `uv` 升级后解释器软链断裂，直接删掉 `.venv` 重建即可（重建后需重跑
`python -m ipykernel install ...`）。
