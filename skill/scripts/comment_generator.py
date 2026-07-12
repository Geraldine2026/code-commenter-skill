#!/usr/bin/env python3
"""
代码注释自动生成器 - 支持 DeepSeek API
"""

import os
import sys
import argparse
from typing import Any, Optional

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请安装 openai: pip install openai")
    sys.exit(1)


class CodeCommenter:
    """代码注释生成器"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # 尝试多种 API Key 来源
        self.api_key = (
            api_key 
            or os.getenv("DEEPSEEK_API_KEY") 
            or os.getenv("OPENAI_API_KEY")
        )
        
        if not self.api_key:
            raise ValueError("未配置 API Key。请设置环境变量 DEEPSEEK_API_KEY")
        
        # 检测使用哪个提供商
        if os.getenv("DEEPSEEK_API_KEY"):
            self.base_url = "https://api.deepseek.com/v1"
            self.model = model or "deepseek-chat"
        else:
            self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            self.model = model or "gpt-3.5-turbo"
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def detect_language(self, code: str) -> str:
        """检测代码语言"""
        if "def " in code or "import " in code or "class " in code:
            return "python"
        elif "function " in code or "const " in code or "let " in code:
            return "javascript"
        elif "public class " in code or "private " in code or "void " in code:
            return "java"
        elif "#include" in code or "int main" in code:
            return "c/c++"
        else:
            return "unknown"
    
    def build_prompt(self, code: str, language: str, style: str, translate_to_en: bool) -> str:
        """构建提示词"""
        lang_name = {
            "python": "Python", "javascript": "JavaScript", 
            "java": "Java", "c/c++": "C/C++"
        }.get(language, language)
        
        prompt = f"""你是一位资深 {lang_name} 开发者，请为以下代码添加专业的中文注释。

要求：
1. 保持原有代码完全不变
2. 添加 {style} 风格的注释
3. 注释应清晰解释：函数/类的用途、参数含义、返回值、核心逻辑、边界条件
4. 注释风格专业、简洁
5. {'同时生成英文版本注释（双语注释）' if translate_to_en else ''}
6. 直接输出添加注释后的完整代码，不要输出任何额外的解释文字

代码：
{code}


请只输出添加注释后的完整代码："""
        return prompt
    
    def generate_comments(self, code: str, language: Optional[str] = None, 
                          style: str = "google", translate_to_en: bool = False) -> str:
        """生成注释"""
        if not language:
            language = self.detect_language(code)
        
        prompt = self.build_prompt(code, language, style, translate_to_en)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的代码注释生成助手，只输出代码，不输出解释。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"❌ 生成失败: {str(e)}"
    
    # 支持的代码文件扩展名
    CODE_EXTENSIONS = {'.py', '.js', '.java', '.c', '.cpp', '.go', '.ts', '.rs', '.tsx', '.jsx', '.cs'}

    def process_file(self, file_path: str, style: str = "google", 
                     translate_to_en: bool = False) -> str:
        """处理单个文件"""
        if not os.path.exists(file_path):
            return f"❌ 文件不存在: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        language = self.detect_language(code)
        result = self.generate_comments(code, language, style, translate_to_en)
        return result

    def process_batch(self, dir_path: str, style: str = "google",
                      translate_to_en: bool = False, output_dir: str = "./output") -> dict[str, Any]:
        """批量处理目录下的所有代码文件。

        递归遍历目录，找到所有支持的代码文件，逐个生成注释，
        并将结果保存到 output_dir 下（保持原有目录结构）。

        Args:
            dir_path: 源代码目录路径。
            style: 注释风格。
            translate_to_en: 是否生成英文注释。
            output_dir: 输出根目录，默认 ./output。

        Returns:
            dict: {"success": 成功数, "fail": 失败数, "total": 总数, "results": 详细列表}
        """
        if not os.path.isdir(dir_path):
            return {"success": 0, "fail": 1, "total": 1, "results": [f"❌ 目录不存在: {dir_path}"]}

        # 递归收集所有代码文件
        files = []
        for root, dirs, filenames in os.walk(dir_path):
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in self.CODE_EXTENSIONS:
                    files.append(os.path.join(root, filename))

        if not files:
            print(f"⚠️ 目录 {dir_path} 下未找到支持的代码文件")
            return {"success": 0, "fail": 0, "total": 0, "results": []}

        # 确保输出根目录存在
        os.makedirs(output_dir, exist_ok=True)

        total = len(files)
        success_count = 0
        fail_count = 0
        results = []

        print(f"\n{'='*60}")
        print(f"🚀 批量处理开始 - 共 {total} 个文件")
        print(f"   输入目录: {dir_path}")
        print(f"   输出目录: {output_dir}")
        print(f"   注释风格: {style}" + (" (英文)" if translate_to_en else ""))
        print(f"{'='*60}\n")

        for i, file_path in enumerate(files, 1):
            print(f"正在处理 [{i}/{total}] {file_path}")

            try:
                if not os.path.exists(file_path):
                    result = f"❌ 文件不存在: {file_path}"
                    fail_count += 1
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()

                    language = self.detect_language(code)
                    commented = self.generate_comments(code, language, style, translate_to_en)

                    # 保持目录结构输出
                    rel_path = os.path.relpath(file_path, dir_path)
                    out_path = os.path.join(output_dir, rel_path)
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)

                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(commented)

                    print(f"  ✅ 已保存 -> {out_path}")
                    result = commented
                    success_count += 1

            except Exception as e:
                print(f"  ❌ 失败: {str(e)}")
                result = f"❌ 失败: {str(e)}"
                fail_count += 1

            results.append({"file": file_path, "result": result})

        # 汇总统计
        print(f"\n{'='*60}")
        print(f"📊 处理完成: 总计 {total} | ✅ 成功 {success_count} | ❌ 失败 {fail_count}")
        print(f"{'='*60}\n")

        return {
            "success": success_count,
            "fail": fail_count,
            "total": total,
            "results": results
        }


    def quality_score(self, code: str, language: str) -> dict:
        """调用 AI 对注释质量进行评分"""
        prompt = f"""你是一位代码审查专家，请对以下 {language} 代码的注释质量进行评分（1-10分）。

评分维度：
1. 完整性：是否涵盖了函数用途、参数、返回值
2. 清晰度：注释是否易于理解
3. 专业性：术语使用是否准确
4. 实用性：是否包含边界条件或使用示例

代码：
{code}

请以 JSON 格式输出：
{{"score": 8.5, "dimensions": {{"completeness": 9, "clarity": 8, "professionalism": 9, "practicality": 8}}, "summary": "优点：... 建议：..."}}

只输出 JSON："""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是代码审查专家，请以 JSON 格式输出评分结果。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return {'score': 0, 'error': str(e)}

    def generate_stats(self, original_code: str, commented_code: str) -> dict:
        """分析代码统计信息"""
        original_lines = original_code.split('\n') if original_code else []
        commented_lines = commented_code.split('\n') if commented_code else []
        
        total_lines = len(commented_lines)
        comment_lines = sum(1 for line in commented_lines 
                          if line.strip().startswith(('#', '//', '/*', '*', '"""', "'''"))
                            or line.strip().startswith('*'))
        # 统计函数/类定义
        import re
        functions = len(re.findall(r'\bdef\s+\w+|\bfunction\s+\w+|\bclass\s+\w+', original_code))
        coverage = round(comment_lines / total_lines * 100, 1) if total_lines > 0 else 0
        
        return {
            'total_lines': total_lines,
            'comment_lines': comment_lines,
            'coverage': coverage,
            'functions': functions
        }


def main():
    parser = argparse.ArgumentParser(description="代码注释自动生成器")
    parser.add_argument("--file", help="代码文件路径")
    parser.add_argument("--code", help="直接输入代码")
    parser.add_argument("--batch", help="批量处理：指定源代码目录路径")
    parser.add_argument("--output-dir", default="./output", help="批量处理时的输出目录（默认 ./output）")
    parser.add_argument("--language", help="编程语言（可选，自动检测）")
    parser.add_argument("--style", default="google", help="注释风格（默认 google）")
    parser.add_argument("--translate-to-en", action="store_true", help="生成英文注释")
    parser.add_argument("--output", help="输出文件路径（单文件模式）")

    parser.add_argument("--format", choices=["code", "markdown"], default="code",
                        help="输出格式：code（纯代码）或 markdown（含代码块）")
    parser.add_argument("--stats", action="store_true",
                        help="显示代码统计信息（行数、注释覆盖率等）")
    parser.add_argument("--quality-score", action="store_true",
                        help="对生成的注释进行质量评分（1-10分）")

    
    args = parser.parse_args()
    
    # 检查输入
    if not args.file and not args.code and not args.batch:
        print("❌ 请提供 --file、--code 或 --batch")
        sys.exit(1)
    
    try:
        commenter = CodeCommenter()
    except ValueError as e:
        print(f"❌ {e}")
        print("请设置: export DEEPSEEK_API_KEY='你的-key'")
        sys.exit(1)
    
    # 批量处理模式
    if args.batch:
        commenter.process_batch(
            dir_path=args.batch,
            style=args.style,
            translate_to_en=args.translate_to_en,
            output_dir=args.output_dir
        )
        return

    # 单文件模式
    if args.file:
        result = commenter.process_file(args.file, args.style, args.translate_to_en)

        language = args.language or commenter.detect_language(result)

    else:
        language = args.language or commenter.detect_language(args.code)
        result = commenter.generate_comments(args.code, language, args.style, args.translate_to_en)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✅ 已保存到: {args.output}")
    else:

        if args.format == "markdown":
            print(f"```{language or 'python'}")
            print(result)
            print("```")
        else:
            print(result)
    
    # 统计信息
    if args.stats:
        original_code = args.code or (open(args.file, encoding='utf-8').read() if args.file else "")
        stats = commenter.generate_stats(original_code, result)
        print_stats_result(stats)
    
    # 质量评分
    if args.quality_score:
        score_result = commenter.quality_score(result, language)
        print_quality_score(score_result)


def print_stats(code: str, language: str, commenter: CodeCommenter):
    """打印统计信息"""
    stats = commenter.generate_stats(code, code)  # 简化版，实际应传 original 和 commented
    
    print("\n" + "=" * 50)
    print("📊 代码分析报告")
    print("=" * 50)
    print(f"📁 文件语言：{language or '未知'}")
    print(f"📝 代码总行数：{stats.get('total_lines', 0)}")
    print(f"💬 注释行数：{stats.get('comment_lines', 0)}")
    print(f"📈 注释覆盖率：{stats.get('coverage', 0)}%")
    print(f"📦 函数/类数量：{stats.get('functions', 0)}")
    print("=" * 50)


def print_stats_result(stats: dict):
    """格式化输出统计信息"""
    print("\n" + "=" * 50)
    print("📊 代码分析报告")
    print("=" * 50)
    print(f"📝 代码总行数：{stats.get('total_lines', 0)}")
    print(f"💬 注释行数：{stats.get('comment_lines', 0)}")
    print(f"📈 注释覆盖率：{stats.get('coverage', 0)}%")
    print(f"📦 函数/类数量：{stats.get('functions', 0)}")
    print("=" * 50)


def print_quality_score(score_result: dict):
    """格式化输出质量评分"""
    if 'error' in score_result:
        print(f"\n❌ 质量评分失败: {score_result['error']}")
        return
    
    print("\n" + "=" * 50)
    print("⭐ 注释质量评分")
    print("=" * 50)
    print(f"📊 综合评分：{score_result.get('score', 0)}/10")
    
    dimensions = score_result.get('dimensions', {})
    if dimensions:
        print("📋 各维度评分：")
        dim_names = {
            'completeness': '完整性',
            'clarity': '清晰度', 
            'professionalism': '专业性',
            'practicality': '实用性'
        }
        for key, name in dim_names.items():
            if key in dimensions:
                print(f"   {name}：{dimensions[key]}/10")
    
    summary = score_result.get('summary', '')
    if summary:
        print(f"💡 评语：{summary}")
    print("=" * 50)

        print(result)



if __name__ == "__main__":
    main()
