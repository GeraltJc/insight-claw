# Issue tracker: GitHub

本项目的需求、缺陷和 PRD 存放在 GitHub Issues 中。所有相关操作默认使用 `gh` CLI。

## 仓库

- GitHub 仓库：`GeraltJc/insight-claw`
- 远程地址：`https://github.com/GeraltJc/insight-claw.git`

在本仓库目录内运行 `gh` 时，通常可以从 `git remote -v` 自动推断目标仓库。

## 约定

- **创建 issue**：使用 `gh issue create --title "..." --body "..."`。多行正文优先使用 heredoc。
- **读取 issue**：使用 `gh issue view <number> --comments`，并按需读取 labels 和 comments。
- **列出 issue**：使用 `gh issue list --state open --json number,title,body,labels,comments`，并按需要增加 `--label` 和 `--state` 过滤。
- **评论 issue**：使用 `gh issue comment <number> --body "..."`
- **添加或移除标签**：使用 `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭 issue**：使用 `gh issue close <number> --comment "..."`

## 当技能说“发布到 issue tracker”

创建一个 GitHub Issue。

## 当技能说“读取相关 ticket”

运行 `gh issue view <number> --comments`。
