# Code Commenter - 智能代码注释生成器

## 选题名称

代码注释自动生成与翻译

## 功能简介

Code Commenter 是一个基于 AI 的代码注释自动生成工具，能够：
- 自动理解代码语义，生成高质量注释
- 支持 Python、JavaScript、Java、C/C++、Go 等多种语言
- 支持 Google Docstring、JSDoc、Javadoc 等多种注释风格
- 支持单文件和批量处理两种模式
- 可选生成中文或双语注释

## AI 核心价值

传统注释工具只能根据函数签名生成空壳注释模板，而 Code Commenter：
- ✅ **理解代码意图**：能解释复杂算法的核心逻辑
- ✅ **生成有意义的说明**：不只是罗列参数，而是解释参数的含义和用途
- ✅ **提供上下文信息**：能说明边界条件、异常情况和使用示例
- ✅ **多语言支持**：自动适配不同语言的注释风格

## 安装

```bash
pip install openai
export DEEPSEEK_API_KEY="your-api-key"
```

## 使用方式

### 单文件处理

```bash
python scripts/comment_generator.py --file path/to/code.py
```

### 直接输入代码

```bash
python scripts/comment_generator.py --code "def add(a, b): return a + b" --language python
```

### 批量处理目录

```bash
python scripts/comment_generator.py --batch ./src --output-dir ./output
```

### 指定注释风格

```bash
python scripts/comment_generator.py --file code.js --style jsdoc
```

## 目录结构

```text
code-commenter/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 项目说明
├── scripts/
│   └── comment_generator.py    # 核心脚本
├── references/
│   ├── prompt_templates.md     # Prompt 模板参考
│   └── config_example.yaml     # 配置文件示例
├── tests/
│   ├── sample_code/            # 测试代码样本
│   └── test_record.md          # 测试记录
└── iteration/
    └── iteration_log.md        # 迭代升级说明
```

## 迭代记录

详见 [iteration/iteration_log.md](iteration/iteration_log.md)

## 测试记录

详见 [tests/test_record.md](tests/test_record.md)

## 许可证

MIT
