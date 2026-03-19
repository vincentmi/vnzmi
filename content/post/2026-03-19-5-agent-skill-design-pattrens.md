---
layout:     post
title:      "每个开发人员都应该了解的5种Agent Skill的设计模式"
date:       "2026-03-19 17:43:00"
author:     "Vincent"
image:      "/img/post-bg-dna.jpg"
tags:
    - python
    - agent
    - skill
    - llama
---

![alt text](/img/in-post/20260319-image.png)

## 前言

> 谈到 𝚂𝙺𝙸𝙻𝙻.𝚖𝚍 文件，开发者往往过于关注格式——确保 YAML 代码正确、目录结构清晰、并严格遵循规范。但如今已有超过 30 种代理工具（例如 Claude Code、Gemini CLI 和 Cursor）采用相同的布局，格式问题实际上已经过时。
> 现在的挑战在于内容设计。规范解释了如何打包一个技能，但对于如何构建其内部逻辑却只字未提。例如，一个封装了 FastAPI 约定的技能与一个四步文档流程的技能，即使它们的 𝚂𝙺𝙸𝙻𝙻.𝚖𝚍 文件看起来完全相同，但它们的运行方式却截然不同。
> 通过研究整个生态系统中技能的构建方式——从 Anthropic 的存储库到 Vercel 和 Google 的内部指南——可以发现五种反复出现的设计模式，这些模式可以帮助开发者构建代理。
>
> 来自 @Saboo_Shubham_ 和 @lavinigam






本文将介绍以下各项功能，并提供可运行的 ADK 代码示例：

- 工具封装器：让您的代理程序瞬间成为任何库的专家
- 生成器：从可重用模板生成结构化文档
- 审阅器：根据严重程度，对照检查清单对代码进行评分
- 反向操作：代理程序在执行操作前会先与您沟通
- 管道：通过检查点强制执行严格的多步骤工作流程

> ADK : Agent Develop Kit   
> https://google.github.io/adk-docs/
> 智能体开发工具包 (ADK) 是一个灵活且模块化的框架，用于开发和部署 AI 智能体。ADK 针对 Gemini 和 Google 生态系统进行了优化，但它与模型和部署方式无关，并且与其他框架兼容。ADK 的设计宗旨是让智能体开发更像软件开发，使开发人员能够更轻松地创建、部署和编排从简单任务到复杂工作流的各种智能体架构。




![alt text](/img/in-post/20260319-image-1.png)
## 模式 1：工具封装器

工具封装器可让您的智能体按需获取特定库的上下文。它无需将 API 约定硬编码到系统提示中，而是将其打包成一个技能。智能体仅在实际使用该技术时才会加载此上下文。

这是最容易实现的模式。```𝚂𝙺𝙸𝙻𝙻.𝚖𝚍``` 文件监听用户提示中的特定库关键字，从 ```𝚛𝚎𝚏𝚎𝚛𝚎𝚗𝚌𝚎𝚜/``` 目录动态加载内部文档，并将这些规则作为绝对真理应用。这正是您将团队内部编码规范或特定框架最佳实践直接融入开发人员工作流程的机制。

以下是一个工具包装器的示例，它教会代理如何编写 FastAPI 代码。请注意，指令如何明确地告诉代理，只有在开始审查或编写代码时才加载 ```𝚌𝚘𝚗𝚟𝚎𝚗𝚝𝚒𝚘𝚗𝚜.𝚖𝚍``` 文件：

```md
# skills/api-expert/SKILL.md
---
name: api-expert
description: FastAPI development best practices and conventions. Use when building, reviewing, or debugging FastAPI applications, REST APIs, or Pydantic models.
metadata:
  pattern: tool-wrapper
  domain: fastapi
---

You are an expert in FastAPI development. Apply these conventions to the user's code or question.

## Core Conventions

Load 'references/conventions.md' for the complete list of FastAPI best practices.

## When Reviewing Code
1. Load the conventions reference
2. Check the user's code against each convention
3. For each violation, cite the specific rule and suggest the fix

## When Writing Code
1. Load the conventions reference
2. Follow every convention exactly
3. Add type annotations to all function signatures
4. Use Annotated style for dependency injection
```

![alt text](/img/in-post/20260319-image-2.png)
## 模式 2：生成器

工具包装器应用知识，而生成器则确保输出的一致性。如果您遇到代理每次运行生成不同文档结构的问题，生成器可以通过协调填空过程来解决这个问题。



它利用了两个可选目录：`𝚊𝚜𝚜𝚎𝚝𝚜/` 存放输出模板，`𝚛𝚎𝚏𝚎𝚛𝚎𝚗𝚌𝚎𝚜/` 存放样式指南。指令集充当项目管理器，指示代理加载模板、读取样式指南、询问用户缺失的变量并填充文档。这对于生成可预测的 API 文档、标准化提交消息或搭建项目架构非常实用。

在本技术报告生成器示例中，技能文件不包含实际的布局或语法规则。它只是协调这些资源的检索，并强制代理逐步执行它们：

```md
# skills/report-generator/SKILL.md
---
name: report-generator
description: Generates structured technical reports in Markdown. Use when the user asks to write, create, or draft a report, summary, or analysis document.
metadata:
  pattern: generator
  output-format: markdown
---

You are a technical report generator. Follow these steps exactly:

Step 1: Load 'references/style-guide.md' for tone and formatting rules.

Step 2: Load 'assets/report-template.md' for the required output structure.

Step 3: Ask the user for any missing information needed to fill the template:
- Topic or subject
- Key findings or data points
- Target audience (technical, executive, general)

Step 4: Fill the template following the style guide rules. Every section in the template must be present in the output.

Step 5: Return the completed report as a single Markdown document.
```

![alt text](/img/in-post/20260319-image-3.png)

## 模式 3：审阅器

审阅器模式将检查内容与检查方法分开。与其编写冗长的系统提示来详细说明每个代码问题，不如将模块化的评分标准存储在 ```𝚛𝚎𝚏𝚎𝚛𝚎𝚗𝚌𝚎𝚜/𝚛𝚎𝚟𝚒𝚎𝚠-𝚌𝚑𝚎𝚌𝚔𝚕𝚒𝚜𝚝.𝚖𝚍``` 文件中。

当用户提交代码时，代理会加载此检查清单，并系统地对提交的代码进行评分，根据严重程度对结果进行分组。如果将 Python 风格的检查清单替换为 OWASP 安全检查清单，您将获得完全不同的、更专业的审计，但使用的却是完全相同的技能基础架构。这是一种高效的自动化 PR 审查或在人工查看代码之前发现漏洞的方法。

以下代码审查技能演示了这种分离。指令保持不变，但代理会动态地从外部检查清单加载特定的审查标准，并强制生成结构化的、基于严重程度的输出：

```md
# skills/code-reviewer/SKILL.md
---
name: code-reviewer
description: Reviews Python code for quality, style, and common bugs. Use when the user submits code for review, asks for feedback on their code, or wants a code audit.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

You are a Python code reviewer. Follow this review protocol exactly:

Step 1: Load 'references/review-checklist.md' for the complete review criteria.

Step 2: Read the user's code carefully. Understand its purpose before critiquing.

Step 3: Apply each rule from the checklist to the code. For every violation found:
- Note the line number (or approximate location)
- Classify severity: error (must fix), warning (should fix), info (consider)
- Explain WHY it's a problem, not just WHAT is wrong
- Suggest a specific fix with corrected code

Step 4: Produce a structured review with these sections:
- **Summary**: What the code does, overall quality assessment
- **Findings**: Grouped by severity (errors first, then warnings, then info)
- **Score**: Rate 1-10 with brief justification
- **Top 3 Recommendations**: The most impactful improvements
```


![alt text](/img/in-post/20260319-image-4.png)

## 模式 4：反向操作

智能体天生倾向于猜测并立即生成答案。反转模式颠覆了这种动态。用户不再提出问题，智能体也不再执行，而是由智能体扮演面试官的角色。

逆向工程依赖于明确且不可协商的门控指令（例如“所有阶段完成后方可开始构建”），强制智能体首先收集上下文信息。它会按顺序提出结构化问题，并在获得您的答案后才进入下一阶段。智能体只有在全面了解您的需求和部署限制后才会生成最终输出。

要查看实际应用，请查看此项目规划器技能。关键在于严格的阶段划分和明确的门控提示，这些提示会阻止智能体在收集到所有用户答案之前生成最终计划：

```md
# skills/project-planner/SKILL.md
---
name: project-planner
description: Plans a new software project by gathering requirements through structured questions before producing a plan. Use when the user says "I want to build", "help me plan", "design a system", or "start a new project".
metadata:
  pattern: inversion
  interaction: multi-turn
---

You are conducting a structured requirements interview. DO NOT start building or designing until all phases are complete.

## Phase 1 — Problem Discovery (ask one question at a time, wait for each answer)

Ask these questions in order. Do not skip any.

- Q1: "What problem does this project solve for its users?"
- Q2: "Who are the primary users? What is their technical level?"
- Q3: "What is the expected scale? (users per day, data volume, request rate)"

## Phase 2 — Technical Constraints (only after Phase 1 is fully answered)

- Q4: "What deployment environment will you use?"
- Q5: "Do you have any technology stack requirements or preferences?"
- Q6: "What are the non-negotiable requirements? (latency, uptime, compliance, budget)"

## Phase 3 — Synthesis (only after all questions are answered)

1. Load 'assets/plan-template.md' for the output format
2. Fill in every section of the template using the gathered requirements
3. Present the completed plan to the user
4. Ask: "Does this plan accurately capture your requirements? What would you change?"
5. Iterate on feedback until the user confirms
```

![alt text](/img/in-post/20260319-image-5.png)

## 模式 5：流水线模式

对于复杂任务，您不能容忍跳过任何步骤或忽略任何指令。流水线模式强制执行严格的顺序工作流程，并设置了硬性检查点。

指令本身即构成工作流程的定义。通过实现明确的菱形门条件（例如，在从文档字符串生成到最终组装之前需要用户批准），流水线模式确保代理无法绕过复杂任务并呈现未经验证的最终结果。

此模式充分利用所有可选目录，仅在需要时才引入不同的参考文件和模板，从而保持上下文窗口的简洁。

在本文档流水线示例中，请注意明确的门控条件。在用户确认上一步生成的文档字符串之前，代理程序被明确禁止进入组装阶段：

```md
# skills/doc-pipeline/SKILL.md
---
name: doc-pipeline
description: Generates API documentation from Python source code through a multi-step pipeline. Use when the user asks to document a module, generate API docs, or create documentation from code.
metadata:
  pattern: pipeline
  steps: "4"
---

You are running a documentation generation pipeline. Execute each step in order. Do NOT skip steps or proceed if a step fails.

## Step 1 — Parse & Inventory
Analyze the user's Python code to extract all public classes, functions, and constants. Present the inventory as a checklist. Ask: "Is this the complete public API you want documented?"

## Step 2 — Generate Docstrings
For each function lacking a docstring:
- Load 'references/docstring-style.md' for the required format
- Generate a docstring following the style guide exactly
- Present each generated docstring for user approval
Do NOT proceed to Step 3 until the user confirms.

## Step 3 — Assemble Documentation
Load 'assets/api-doc-template.md' for the output structure. Compile all classes, functions, and docstrings into a single API reference document.

## Step 4 — Quality Check
Review against 'references/quality-checklist.md':
- Every public symbol documented
- Every parameter has a type and description
- At least one usage example per function
Report results. Fix issues before presenting the final document.
```



## 选择合适的代理技能模式

每种模式都回答不同的问题。请使用此决策树找到适合您用例的模式：

![alt text](/img/in-post/20260319-image-6.png)


## 最后，模式可以组合。

这些模式并非互斥，而是可以组合。

管道技能可以在最后添加一个审核步骤，以再次检查自身的工作。生成器可以在最开始依赖反转来收集必要的变量，然后再填充其模板。得益于 ADK 的 𝚂𝚔𝚒𝚕𝚕𝚃𝚘𝚘𝚕𝚜𝚎𝚝 和渐进式披露，您的代理仅在运行时使用所需的精确模式来分配上下文令牌。

不要再试图将复杂且脆弱的指令塞进单个系统提示中。分解您的工作流程，应用正确的结构模式，构建可靠的代理。

## 立即开始

代理技能规范是开源的，并且在 ADK 中得到原生支持。您已经知道如何打包格式。现在您知道如何设计内容了。使用 Google Agent Development Kit 构建更智能的代理吧。
