# Prompt 模板参考

## 概述

本文档记录了 code-commenter skill 使用的提示词模板，供优化和调试参考。

## 当前使用的 Prompt（v1.1）

经过两轮迭代优化，当前使用的 prompt 如下：
你是一位资深 {lang_name} 开发者，请为以下代码添加专业注释。

严格要求：

1. 保持原有代码完全不变，不修改任何代码逻辑

2. 注释风格必须使用 Google 风格中文 Docstring

3. 标签必须使用英文：Args:、Returns:、Raises:、Examples:

4. 标签后的说明使用中文

5. 必须包含：函数用途、参数说明、返回值说明

6. 可选包含：异常说明、使用示例

7. 直接输出完整的带注释代码，不要输出任何额外的解释文字

8. 确保输出完整，不要截断

## 各语言注释风格示例

### Python - Google 风格

```python
def fibonacci(n):
    """计算斐波那契数列的第n项。
    
    Args:
        n (int): 非负整数，表示要计算的项数索引。
    
    Returns:
        int: 斐波那契数列的第n项值。
    
    Raises:
        RecursionError: 当n过大时，可能导致递归深度超过Python限制。
    
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(5)
        5
    """
```

### JavaScript - JSDoc 风格

```javascript
/**
 * 快速排序函数
 * 使用递归方式对数组进行排序，基于分治策略
 * 
 * @param {Array} arr - 待排序的数组
 * @returns {Array} 排序后的新数组
 */
```

### Java - Javadoc 风格

```java
/**
 * 计算两个整数的商。
 * 
 * @param a 被除数
 * @param b 除数
 * @return 返回 a 除以 b 的整数商
 * @throws IllegalArgumentException 如果除数为零
 */
```

## 迭代历史

| 版本 | 变更内容 |
|------|----------|
| v1.0 | 初始 prompt，风格不统一 |
| v1.1 | 统一标签格式，增加输出完整性要求 |

## 最佳实践建议

- 保持 prompt 简洁明确
- 使用负面约束（"不要..."）比正面约束更有效
- 适当降低 temperature（0.3）保证输出稳定性
- 设置足够的 max_tokens 避免截断
