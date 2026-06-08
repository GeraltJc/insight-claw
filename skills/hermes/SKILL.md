---
name: hermes
description: "Use when Hermes Agent receives a request to analyze A-share stocks with Insight Claw, including Chinese requests like 分析 600519 股票, 分析 贵州茅台, 分析 600519,000001, 生成这些 A 股的分析报告, or when the user asks to run local stock analysis and return generated reports."
---

# Insight Claw 股票分析

## 目标

使用当前 Insight Claw 项目的本地 CLI，为用户分析一个或多个 A 股标的，并返回生成报告中的关键结论。

这个 skill 给 Hermes Agent 使用。不要把它解释成项目内存在 `hermes` shell 命令，也不要默认启用项目里尚未完整接通的 Agent 模式。

## 触发场景

当用户表达以下意图时使用本 skill：

- “分析 600519 股票”
- “分析 贵州茅台”
- “分析 600519,000001”
- “用 Insight Claw 分析这些股票”
- “生成这些 A 股的分析报告”
- “跑一下我的自选股分析”

如果用户只是询问项目架构、配置说明或代码实现，不要运行分析命令；先回答问题或检查相关文件。

## 前置检查

1. 确认当前工作目录是 Insight Claw 仓库根目录。仓库根目录应包含 `justice_plutus/cli.py`、`src/core/pipeline.py` 和 `README.md`。
2. 确认用户提供了股票代码或股票名称。
3. 确认可用的 Python 环境能导入项目依赖。
4. 确认至少配置一种 LLM key 路径，例如 `OPENAI_API_KEY`、`AIHUBMIX_KEY`、`GEMINI_API_KEY`、`ANTHROPIC_API_KEY` 或 `DEEPSEEK_API_KEY`。

缺少 `TUSHARE_TOKEN`、`BOCHA_API_KEYS`、`TAVILY_API_KEYS`、`SERPAPI_API_KEYS`、`WENCAI_COOKIE` 或 iFinD 相关变量时，不要直接阻塞基础分析；这些是增强能力。

## 股票输入处理

优先使用用户明确给出的 6 位 A 股代码。多个代码用英文逗号连接，例如：

```text
600519,000001
```

如果用户给的是股票名称，先尝试在项目的股票映射或已有数据源中找到对应代码。无法确认代码时，向用户询问，不要猜测。

## 默认执行命令

默认只生成本地报告，不发送通知：

```bash
python -m justice_plutus run --stocks "<codes>" --no-notify
```

示例：

```bash
python -m justice_plutus run --stocks "600519" --no-notify
```

批量示例：

```bash
python -m justice_plutus run --stocks "600519,000001" --no-notify
```

如果用户明确要求推送、发送通知、发送到飞书、Telegram 或其它已配置渠道，去掉 `--no-notify`：

```bash
python -m justice_plutus run --stocks "<codes>"
```

## 报告读取

命令完成后，检查最新的 `reports/YYYY-MM-DD/` 输出目录。

优先读取：

```text
reports/YYYY-MM-DD/summary.md
```

用户要求单股细节时，再读取：

```text
reports/YYYY-MM-DD/stocks/<code>.md
```

回复用户时包含：

- 股票代码和股票名称
- 核心结论
- 操作建议
- 主要风险
- 报告文件路径

不要编造报告中不存在的价格、评分、建议或数据源。

## 错误处理

如果命令失败，报告以下信息：

1. 失败命令
2. 关键错误行
3. 最可能原因
4. 下一步修复方式

常见处理：

- `ModuleNotFoundError`：提示用户安装项目依赖。
- “未提供股票列表”：要求用户提供股票代码或配置 `STOCK_LIST`。
- LLM key 缺失：提示至少配置一种 LLM key。
- 数据源失败：说明可能仍可生成降级报告，并检查报告目录是否已有输出。
- 报告目录不存在：说明 CLI 未成功生成报告，保留错误输出供用户排查。
- 通知失败：说明本地报告是否已生成，并提示检查对应通知环境变量。

## Agent 模式边界

不要默认设置：

```bash
AGENT_MODE=true
```

当前仓库存在 Agent 模式相关分支，但完整 executor 不在当前代码树中。除非仓库后续补齐 Hermes 或 Agent executor，并且用户明确要求测试高级 Agent 模式，否则始终使用 `python -m justice_plutus run` 本地 CLI。
