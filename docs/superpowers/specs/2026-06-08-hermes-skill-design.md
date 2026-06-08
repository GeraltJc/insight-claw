# Hermes Skill 设计

## 目标

创建一个随 Insight Claw 项目发布的 skill，供 Hermes Agent 用户通过自然语言请求运行股票分析，例如“分析 600519 股票”。

这个 skill 的使用者是 Hermes Agent。Codex 只在当前开发过程中用于编写和验证该 skill。

## 范围

skill 文件放在：

```text
skills/hermes/SKILL.md
```

它需要指导 Hermes Agent 完成以下工作：

- 识别股票分析请求
- 尽可能把用户输入的股票名称或股票代码规范成股票代码
- 运行现有 Insight Claw 本地 CLI
- 读取生成的 Markdown 报告
- 向用户返回简洁的分析摘要
- 诊断常见配置和运行错误

初始版本不新增运行时代码，也不新增包装脚本。当前仓库已经提供可用的 CLI 入口：

```bash
python -m justice_plutus run --stocks "600519" --no-notify
```

## 触发行为

skill 应该在以下类型的用户请求中触发：

- “分析 600519 股票”
- “分析 贵州茅台”
- “分析 600519,000001”
- “用 Insight Claw 分析这些股票”
- “生成这些 A 股的分析报告”

只要用户意图明确是股票分析，就不应该要求用户必须提到 Hermes、Insight Claw 或 JusticePlutus。

## 执行流程

Hermes Agent 应该：

1. 确认当前工作目录是 Insight Claw 仓库根目录。
2. 从用户请求中提取股票代码或股票名称。
3. 在可行时，把股票输入规范成逗号分隔的 6 位 A 股代码。
4. 默认运行本地分析，不发送通知：

   ```bash
   python -m justice_plutus run --stocks "<codes>" --no-notify
   ```

5. 只有当用户明确要求推送或发送通知时，才去掉 `--no-notify`。
6. 运行结束后，检查 `reports/YYYY-MM-DD/` 下生成的报告目录。
7. 批量结果优先读取 `summary.md`；当用户要求单股细节时，再读取 `stocks/<code>.md`。
8. 回复用户时给出可执行的分析结论和报告文件路径。

## 配置指引

skill 只描述 Hermes Agent 在运行前需要检查的配置：

- Python 3.11+ 和项目依赖已经安装
- 至少存在一种可用的 LLM key 路径，例如 `OPENAI_API_KEY`、`AIHUBMIX_KEY`、`GEMINI_API_KEY`、`ANTHROPIC_API_KEY` 或 `DEEPSEEK_API_KEY`
- 可选的数据和搜索增强配置，例如 `TUSHARE_TOKEN`、`BOCHA_API_KEYS`、`TAVILY_API_KEYS`、`SERPAPI_API_KEYS`、`WENCAI_COOKIE` 以及 iFinD 相关变量
- 可选通知配置，仅在用户要求推送时使用

缺少可选增强配置时，不应阻塞基础本地报告生成。

## Hermes Agent 边界

这个 skill 命名为 `hermes`，是因为它由 Hermes Agent 消费。它不能声称当前仓库已经提供 `hermes` shell 命令，也不能声称当前仓库已经提供完整 Hermes 运行时。

当前仓库在 `src/core/pipeline.py` 中有 Agent 模式分支，但该分支引用的 executor 模块在当前代码树中不存在。因此，skill 不应默认启用 `AGENT_MODE=true`。如果项目未来补齐完整 Hermes 或 Agent executor，可以在后续版本中把这条路径记录为可选高级模式。

## 错误处理

skill 应该指导 Hermes Agent 诊断以下问题：

- 项目依赖缺失或 Python import 失败
- 用户没有提供股票输入
- 缺少必需的 LLM 凭证
- 数据源失败，但仍可生成降级报告
- LLM 失败，导致分析失败或只生成占位内容
- CLI 退出后没有找到报告输出
- 用户要求推送时通知发送失败

Hermes Agent 应该报告失败命令、关键错误行和下一步具体修复方式。它不应该把运行失败包装成泛泛的成功回复。

## 文件结构

初始实现：

```text
skills/
└── hermes/
    └── SKILL.md
```

第一版不需要 `references/`、`scripts/` 或 `assets/` 目录。只有当 skill 内容增长到不适合单文件维护时，才再拆分辅助资源。

## 验证方式

验证 skill 时需要确认：

- YAML frontmatter 只包含 `name` 和 `description`
- skill 路径符合公开项目布局要求
- 面向 Hermes 的 skill 中没有残留 Codex 专属指令
- 运行命令与当前仓库 CLI 一致
- 如果可用，运行 skill 校验工具

