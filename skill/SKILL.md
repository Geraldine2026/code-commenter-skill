---
name: code-commenter
description: 自动为代码生成智能注释，支持多语言。当用户需要为代码添加注释、生成文档注释、或对已有代码进行注释补全时，使用此 skill。支持通过文件路径或直接粘贴代码进行注释生成。
version: 1.0.0
---

# Code Commenter

## Overview

Code Commenter 是一个代码注释自动生成工具，支持为多种编程语言的代码智能添加注释。用户可以通过指定文件路径或直接粘贴代码片段，AI 自动分析代码逻辑并生成清晰、规范的注释。支持 Google Style、JSDoc、JavaDoc 等多种注释风格，并可选择生成英文注释。

## When to Use

This skill should be used when:
- 用户要求为某段代码或某个文件添加注释
- 用户需要生成 API 文档注释（如 JSDoc、JavaDoc）
- 用户希望将无注释的代码补充完整注释
- 用户提到 `--file`、`--code`、`--style` 等参数
- 用户想将中文注释翻译为英文注释

## Supported Languages

- Python
- JavaScript / TypeScript
- Java
- C++
- Go
- Rust
- 以及其他常见编程语言

## Usage

### Command Parameters

| 参数 | 说明 | 示例 |
|------|------|------|
| `--file` | 指定文件路径，为整个文件生成注释 | `--file ./src/main.py` |
| `--code` | 直接输入代码字符串，为代码片段生成注释 | `--code "def foo(): pass"` |
| `--style` | 指定注释风格，支持 `google`、`jsdoc`、`javadoc` | `--style jsdoc` |
| `--translate-to-en` | 将生成的注释翻译为英文 | `--translate-to-en` |

### Comment Styles

- **google**: Google Python/Java style docstrings, 紧凑清晰，适合大多数场景
- **jsdoc**: JSDoc 风格，适用于 JavaScript/TypeScript，支持 `@param`、`@returns` 等标签
- **javadoc**: JavaDoc 风格，适用于 Java，支持 `@param`、`@return`、`@throws` 等标签

### Example Workflow

1. **通过文件路径生成注释**

   用户输入：
   ```
   请为这个文件添加注释 --file ./src/utils.py --style google --translate-to-en
   ```

   - 读取 `./src/utils.py` 文件内容
   - 分析代码结构和逻辑
   - 按照 Google Style 为每个函数、类、模块生成英文注释
   - 返回带注释的完整代码或修改原文件

2. **直接粘贴代码生成注释**

   用户输入：
   ```
   为以下代码添加 JavaDoc 注释 --code "..." --style javadoc
   ```

   - 解析粘贴的代码
   - 按照 JavaDoc 风格生成注释
   - 输出带注释的代码

## Comment Generation Guidelines

生成注释时，应遵循以下原则：

1. **函数/方法注释**：说明功能、参数含义、返回值类型和含义，必要时补充异常情况
2. **类注释**：说明类的用途、设计意图和主要职责
3. **模块注释**：说明模块的整体功能和包含的主要内容
4. **复杂逻辑注释**：对关键算法、非直观的代码段添加行内注释
5. **避免冗余**：不为显而易见的代码（如 `x = x + 1`）添加注释
6. **保持简洁**：注释应精炼，直接说明「做什么」和「为什么」，而非逐行描述代码

## Resources

### scripts/
存放注释生成过程中可复用的辅助脚本。

### references/
存放注释风格规范、语言特定注释模板等参考文档。

### tests/sample_code/
存放用于测试注释生成效果的示例代码文件。
