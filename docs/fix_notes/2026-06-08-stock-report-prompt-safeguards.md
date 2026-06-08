# 股票分析报告 Prompt 与口径修复记录

## 背景

本次修复针对 `603986` 投资分析报告排查中发现的几个问题：

- 未提供筹码分布数据时，LLM 仍可能输出获利比例、平均成本、筹码集中度等筹码分析。
- 均线形态判断口径不一致，一处使用 `close > MA5 > MA10 > MA20`，另一处使用 `MA5 > MA10 > MA20`。
- 在缺少资金流、盘口、龙虎榜、筹码数据时，量能解读可能推断到“主力资金”“洗盘”等无法由现有数据支撑的结论。
- 单日大跌且收盘跌破 MA5 时，报告仍可能因为均线多头排列或系统评分偏高给出偏乐观买入建议。

对应提交：

```text
c68af66 fix: tighten stock report prompt safeguards
```

## 修复内容

### 1. 筹码数据缺失时禁止编造

修改文件：[src/analyzer.py](/Users/jc/projects/insight-claw/src/analyzer.py)

主要改动：

- 在系统 prompt 中明确：只有提供真实筹码分布数据时才允许填写筹码数值。
- 无筹码数据时，要求 `chip_structure` 输出为 `null`。
- 在用户 prompt 中新增“筹码分布数据缺失”提示，要求不得推断或编造获利比例、平均成本、筹码集中度。
- 行动检查清单中，筹码项必须标记为“数据缺失，无法判断”。

预期效果：

- 报告不会再把不存在的筹码数据包装成确定性结论。
- 用户可以清楚看到筹码分析不可用，而不是误以为系统已经获取到筹码分布。

### 2. 统一均线形态判断口径

修改文件：

- [src/storage.py](/Users/jc/projects/insight-claw/src/storage.py)
- [src/core/pipeline.py](/Users/jc/projects/insight-claw/src/core/pipeline.py)

主要改动：

- “多头排列”统一定义为 `MA5 > MA10 > MA20`。
- “空头排列”统一定义为 `MA5 < MA10 < MA20`。
- 收盘价与 MA5 的关系不再混入均线排列判断，改由乖离率、支撑位、风险降级等逻辑单独处理。

预期效果：

- 均线形态专注描述均线之间的排列关系。
- 避免出现同一组数据在不同模块中分别被判为“多头排列”和“震荡整理”的情况。

### 3. 限制量能过度解读

修改文件：[src/analyzer.py](/Users/jc/projects/insight-claw/src/analyzer.py)

主要改动：

- 在系统 prompt 中增加“量能解读边界”：
  - 没有资金流、盘口、龙虎榜或筹码数据时，只能描述量比、成交量变化、换手率等客观现象。
  - 不得判断“主力资金未出货”“正常洗盘”“主力吸筹”“主力出货”。

预期效果：

- 降低 LLM 从量价数据直接推断主力意图的概率。
- 报告展示层避免出现缺少数据支撑的资金行为判断。

当前边界：

- 最新重跑中，最终 Markdown 报告未展示“主力未出货/洗盘”等结论。
- 但 LLM 原始 JSON 的非展示字段仍出现过类似“主力或借业绩利好兑现部分筹码”的表述。
- 如果要彻底约束，需要增加确定性的后处理清洗或字段校验，而不能只依赖 prompt。

### 4. 大跌破 MA5 时降级买入结论

修改文件：[src/analyzer.py](/Users/jc/projects/insight-claw/src/analyzer.py)

主要改动：

- 在系统 prompt 中增加“大跌破短均线降级”规则：
  - 单日跌幅达到或超过 5%，且收盘价低于 MA5 时，短线支撑尚未确认。
  - 即使 `MA5 > MA10 > MA20` 或系统评分偏高，也不得直接给出买入/加仓。
  - 若输出狙击点，必须写明触发条件，例如重新站回 MA5、缩量企稳、次日不再创新低。
- 新增 `_apply_market_consistency_guards()` 确定性守卫：
  - 当 LLM 输出 `decision_type == "buy"`，且 `pct_chg <= -5`，且 `close < ma5` 时，自动降级为 `hold`。
  - 同步更新操作建议、置信度、核心信号和检查清单。

预期效果：

- 不再完全依赖 LLM 自觉遵守风险规则。
- 对明显冲突的“买入”结论进行程序化降级。

## 测试覆盖

新增和更新测试：

- [tests/test_ifind_analyzer_prompt.py](/Users/jc/projects/insight-claw/tests/test_ifind_analyzer_prompt.py)
  - 验证无筹码数据时 prompt 明确标记缺失。
  - 验证系统 prompt 允许 `chip_structure: null`。
  - 验证系统 prompt 禁止在无资金流等数据时推断主力行为。
  - 验证大跌跌破 MA5 时禁止直接买入。
  - 验证确定性守卫会把买入降级为观望。
- [tests/test_ma_status.py](/Users/jc/projects/insight-claw/tests/test_ma_status.py)
  - 验证 storage 与 pipeline 均使用 `MA5 > MA10 > MA20` 判断多头排列。
  - 覆盖 `close < MA5` 但均线仍为多头排列的场景。

验证命令：

```bash
.venv/bin/python -m pytest
```

验证结果：

```text
69 passed in 2.53s
```

## 重跑验证

重跑命令：

```bash
.venv/bin/python -m justice_plutus run --stocks 603986 --no-notify
```

关键结果：

- 报告生成成功：[reports/2026-06-08/summary.md](/Users/jc/projects/insight-claw/reports/2026-06-08/summary.md)
- 汇总结果为 `买入:0 观望:1 卖出:0`。
- `603986` 最终操作建议为 `观望`，评分 `58`。
- 筹码检查项显示“数据缺失，无法判断”。
- 均线展示为 `MA5(494.45)>MA10(493.06)>MA20(452.03)`，口径为“多头排列”。

## 后续建议

本次已修复主要 prompt 约束和关键口径冲突，但仍建议继续处理两个确定性风险：

- 对 LLM 原始 JSON 增加字段级校验，发现“主力”“洗盘”“吸筹”“出货”等禁用词且缺少资金流/盘口/龙虎榜/筹码数据时，自动清洗或降级。
- 对 `volume_status` 增加程序化口径，例如按量比、成交量变化、换手率分别输出，避免 LLM 将“高成交额”和“放量”混用。
