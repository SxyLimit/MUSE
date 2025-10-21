# 本文件汇集任务复盘阶段的提示词，涵盖经验总结、工具改进与指南合并等场景
# 总结成功与失败经验的提示词：用于归纳可复用的成功经验和失败反思
# 中文翻译：
# """
# 任务目标：
# 基于本次任务的执行情况，总结成功子任务的**经验教训**以及失败子任务的**反思**，以便在后续任务中复制成功模式、避开失败陷阱。
#
# 写作要求：
# 1. 成功子任务总结：
#     - 明确任务背景与目标
#     - 找出关键成功因素（流程、策略、工具选择、沟通方式等）
#     - 识别可复用的实践或模式
# 2. 失败子任务反思：
#     - 简述失败原因（包括过程中的关键错误或缺陷）
#     - 分析底层问题（如信息不足、误判、执行偏差等）
#     - 提出有针对性的改进建议或替代策略
# 3. 内容必须基于真实任务经验，避免空洞或不可执行的描述。
# 4. 每条总结或反思都应能为未来任务提供直接指导。
# 5. 若某子任务部分成功、部分失败，可分别记录在“成功经验”和“失败反思”中。
# """
summarize_success_and_failure_prompt = """\
Task Objective:
Based on the execution of this task, summarize the **lessons learned** from successful subtasks and **reflections** from failed subtasks, so that successful models can be replicated and failure pitfalls avoided in subsequent tasks.

Writing Requirements:
1. Summary of Successful Subtasks:
    - Clarify the task context and objectives
    - Identify key success factors (process, strategy, tool selection, communication methods, etc.)
    - Identify reusable practices or patterns
2. Reflection of Failed Subtasks:
    - Briefly describe the reasons for failure (including key errors or flaws in the process)
    - Analyze the underlying issues (such as insufficient information, misjudgment, execution deviations, etc.)
    - Provide targeted improvement suggestions or alternative strategies
3. Content must be based on real-world task experiences; avoid empty or unactionable descriptions.
4. Each summary or reflection should provide direct guidance for future tasks.
5. If a subtask is partially successful and partially unsuccessful, it can be separated into "Successful Lessons" and "Reflections on Failures" for separate recording.
"""

# 工具描述优化提示词：指导根据本次任务的实际使用情况完善工具说明与指令
# 中文翻译：
# """
# 任务目标：
# 基于本次任务中各工具的实际使用情况，回顾、总结并优化它们的工具描述与工具指令。
#
# 术语定义：
# - 工具描述：
#     概述工具的整体功能、主要用途、适用场景、注意事项或其他重要信息，帮助使用者理解工具的价值与限制。
# - 工具指令：
#     工具执行完毕后，Observation 中附带的后续指令，通常用于指导下一步操作或限制后续行为，对下一次行动影响最大。
#
# 输入：
# - 现有的工具描述与工具指令，格式如下：
# <tools>
# {tools}
# </tools>
#
# 任务要求：
# 1. 仅在现有字典基础上修改或新增，勿重复写入未变更的条目。
# 2. 优化内容包括：
#     - 补充缺失的重要功能信息
#     - 更正不准确或含糊的描述
#     - 添加在实际使用中发现的注意事项
#     - 优化语言，使其更精炼、准确、易懂
# 3. 输出格式为 JSON，最终结果将用于对原字典执行 `update` 操作。
# 4. **不要**输出不想修改的条目。
#
# 最终输出格式（JSON 代码块需置于最后，单独成段）：
# ```json
# {{
#     "<tool_name>": {{
#         "tool_description": "<用于提供参考的工具描述>",
#         "tool_instruction": "<工具执行结束后附带在 observation 中的指令>"
#     }}
#     ···
# }}
# ```
# 注意：
# 你可以在 JSON 输出前加入任意长度的思考、总结或提炼内容。
# 但 JSON 代码块必须格式正确并独立输出，以便后续解析。
# """
reflect_tool_enhance_prompt = """\
Task Objective:
Based on the actual usage of each tool in this task, review, summarize, and optimize their tool descriptions and tool instructions.

Term Definitions:
- Tool Description:
    This summarizes the tool's overall functionality, primary purpose, applicable scenarios, precautions, or other important tool-related information. This helps the user understand the tool's value and limitations.
- Tool Instruction:
    After the specific tool completes execution, the post-execution instructions included in the observation are typically used to guide the next step or restrict subsequent behavior, and have the most significant impact on the next action.

Input:
- Existing tool descriptions and tool instructions, in the following format:
<tools>
{tools}
</tools>

Task Requirements:
1. Modify or add only to the existing dictionary; do not re-enter unchanged entries.
2. Optimizations should include:
    - Adding missing important functional information
    - Correcting inaccurate or ambiguous descriptions
    - Adding precautions discovered during actual use
    - Optimizing the language to make it more concise, precise, and easy to understand
3. The output format is JSON, and the final result will be used to perform an `update` operation on the original dictionary.
4. **DO NOT** output any entries you do not want to modify.

Final output format (JSON block must be placed last and occupy a separate paragraph):
```json
{{
    "<tool_name>": {{
        "tool_description": "<description of the tool used to give you a reference>",
        "tool_instruction": "<After the tool has finished executing, the instruction attached to the observation>"
    }}
    ···
}}
```
Note:
You can include any length of thought, summary, or refinement before the JSON output.
However, the JSON block must be formatted correctly and output independently to facilitate subsequent parsing.
"""

# 方法论提炼提示词：引导分析疑难场景并总结可复用的解决模式
# 中文翻译：
# """
# 任务目标：
# 回顾本次任务中遇到的难题——尤其是那些推进困难、需要多次尝试才突破的情境。
# 你需要深入分析与反思这些情境，然后输出一个包含“解决模式”的结构化 JSON 块，以便后续解析和复用。
#
# 分析与总结阶段（可适当展开以帮助提炼模式）：
# 1. 详细回顾每个难题的背景与过程。
# 2. 分析造成困境的核心原因（为何难以推进）。
# 3. 记录最终促成成功的关键做法（哪些方法/策略/决策奏效）。
# 4. 思考这些做法在不同情境下的适用性，并找出可复用的模式或范式。
# 5. 用精炼、通用的语言表达这些模式，同时配上简短说明，避免空洞口号。
#
# 输出阶段（严格的格式要求）：
# - 最终输出必须包含一个独立的 JSON 代码块，便于解析。
# - 每个模式都需明确指向一个可复用的解决方案或方法，不能仅陈述事实。
# - 优先提炼**通用范式**，同时保留简短的说明以提供上下文。
#
# 最终输出格式（JSON 代码块需置于最后，单独成段）：
# ```json
# {
#     "<pattern_key>": "<模式陈述 + 简短说明>",
#     ...
# }
# ```
# 注意：
# 你可以在 JSON 输出前撰写任意长度的思考、总结或提炼内容。
# 但 JSON 代码块必须格式正确并独立输出，以便后续解析。
# """
reflect_methodology_enhance_prompt = """\
Task Objective:
Reflect on the dilemmas encountered during this task — especially those that were difficult to advance and required multiple attempts to overcome.
You will need to thoroughly analyze and reflect on the situation, then output a structured JSON block containing the "Resolution Patterns" for parsing and subsequent reuse.

Analysis and Summary Phase (feel free to expand to help you refine patterns):
1. Review the context and process of each dilemma in detail.
2. Analyze the core cause of the dilemma (why progress was difficult).
3. Document the key practices that ultimately led to a successful resolution (what methods/strategies/decisions worked).
4. Consider whether these practices are still effective in different contexts and identify reusable patterns or paradigms.
5. Express these patterns in concise, universal language so they can be applied to subsequent tasks, while keeping a short explanatory note to avoid them being empty slogans.

Output Phase (strict formatting requirements):
- Your final output must include a separate JSON block for parsing.
- Each pattern should clearly point to a reusable solution or approach, rather than simply stating facts.
- Prioritize identifying **universal paradigms** while retaining explanatory notes for context.

Final output format (JSON block must be placed last and occupy a separate paragraph):
```json
{
    "<pattern_key>": "<pattern_statement + short explanatory note>",
    ...
}
```
Note:
You can include any length of thought, summary, or refinement before the JSON output.
However, the JSON block must be formatted correctly and output independently to facilitate subsequent parsing.
"""

# 方法论合并提示词：用于将历史与新增的解决模式归并、去重并统一表述
# 中文翻译：
# """
# # 背景 #
# 你是 **解决模式合并专家**。
# 你的唯一职责是整合并统一两组“解决模式”：
# 1. **既有模式**（此前积累）
# 2. **新模式**（最近从困境反思中提炼）
#
# # 目标 #
# - 将**既有模式**与**新模式**合并成一个 JSON 代码块。
# - 确保合并后的版本**一致、无冗余，且最多保留 10 项**。
# - 每一项都必须表述为**通用、可复用的模式**（而非任务特有事实）。
# - 若新旧模式存在相似内容，请合并为一个更完善、泛化的模式。
# - 若旧有条目已过时或被新洞见推翻，请删除或优化。
#
# # 深度要求 #
# - 每条模式需简洁但有内涵：
#   - **模式键保持 2–6 个词**。
#   - 每条说明必须包含**行动/方法**与**简短原理**（为何重要/如何发挥作用）。
#   - 避免泛泛口号；务必明确“做什么”和“为什么”。
#
# # 输入 #
# - 现有“解决模式”：
# <Old Resolution Patterns>
# {old_methodology}
# </Old Resolution Patterns>
# - 新的“解决模式”：
# <New Resolution Patterns>
# {new_methodology}
# </New Resolution Patterns>
#
# # 输出格式 #
# 最终输出格式（JSON 代码块需置于最后，单独成段）：
# ```json
# {{
#     "<pattern_key>": "<模式陈述 + 简短原理>",
#     ...
# }}
# ```
# 注意：
# 你可以在 JSON 输出前加入任意长度的思考、总结或提炼内容。
# 但 JSON 代码块必须格式正确并独立输出，以便后续解析。
#
# # 规则 #
# - 保持模式清晰、简洁，并适用于不同任务。
# - 避免重复：将重叠观点合并成更强的统一模式。
# - 总数最多 10 条。
# - 每条模式必须兼顾清晰与原理，不可过于抽象。
# """
merge_methodology_prompt = """\
# CONTEXT #
You are the **Resolution Patterns Merge Expert**.
Your sole responsibility is to integrate and unify two sets of "Resolution Patterns":  
1. **Existing Patterns** (previously accumulated)  
2. **New Patterns** (newly extracted from recent dilemmas and reflections)  

# OBJECTIVE #
- Merge the **existing patterns** with the **new patterns** into a single JSON block.  
- Ensure the merged version is **consistent, non-redundant, and limited to a maximum of 10 items**.  
- Each item must be phrased as a **universal, reusable pattern** (not task-specific facts).  
- If new and old contain similar patterns, consolidate them into one improved, generalized pattern.  
- If any old item is outdated or contradicted by newer insights, remove or refine it.  

# DEPTH REQUIREMENT #
- Each pattern must be concise but meaningful:  
  - Keep the **pattern key short (2–6 words)**.  
  - Each statement must contain both **the action/approach** and **a short rationale** (why it matters / how it helps).  
  - Avoid generic slogans; ensure clarity of both “what to do” and “why to do it.”  

# INPUT #
- Existing "Resolution Patterns":
<Old Resolution Patterns>
{old_methodology}
</Old Resolution Patterns>
- New "Resolution Patterns":
<New Resolution Patterns>
{new_methodology}
</New Resolution Patterns>

# Output Format #
Final output format (JSON block must be placed last and occupy a separate paragraph):
```json
{{
    "<pattern_key>": "<pattern_statement + short rationale>",
    ...
}}
Note:
You can include any length of thought, summary, or refinement before the JSON output.
However, the JSON block must be formatted correctly and output independently to facilitate subsequent parsing.

# RULES #
- Keep patterns clear, concise, and applicable across different tasks.
- Avoid duplication: merge overlapping ideas into stronger unified patterns.
- Maximum of 10 items total.
- Each pattern must balance clarity + rationale, not just abstract phrasing.
"""

# 平台/应用指南合并提示词：负责对操作指南进行归并、规范化与质量提升
# 中文翻译：
# """
# # 背景 #
# 你是 **应用操作指南合并专家**。
# 你的职责是对“平台/应用操作指南”字典进行**合并、去重、规范化与质量提升**。
#
# # 输入 #
# - 当前的“Platform/Application Operation Guides”：
# <Platform/Application Operation Guides>
# {guidance}
# </Platform/Application Operation Guides>
#
# # 目标 #
# - 识别并合并相似/重复的操作步骤。
# - 将平台/应用名称规范为标准写法。
# - 改进表述不清或质量较低的步骤，使其简洁明确、可复用。
#
# # 合并与改进规则 #
# 1. 平台标准化
#     - 将同一平台的不同别名/变体合并为统一规范名称。
#     - 例如：`FastAPI Code Development` / `FastAPI Deployment` → `FastAPI`。
#     - 使用一致的大小写与命名（如 GitLab、FastAPI、RocketChat）。
# 2. 按操作意图聚类
#     - 按操作目的对条目分组。
#     - 例如：create/add/new → Create；start/run/launch → Start。
# 3. 整合
#     - 保留最清晰、最通用的操作名称。
#     - 合并步骤，移除冗余，优先采用可靠且安全的版本。
# 4. 前置条件与注意事项
#     - 若操作依赖特定条件，在开头添加 `preconditions`。
#     - 若存在风险或注意事项，在结尾添加 `notes`。
# 5. 表述清晰
#     - 使用精准的动作描述。例如：用 `Click "New Issue" Button` 替代 `Click Button`，将含糊的 `parsing` 细化为 `直接观察提取` 或 `基于 Python 的解析`。
# 6. 术语与风格
#     - 采用一致的祈使句式：`Open -> Select -> Configure -> Save -> Verify`。
# 7. 不得杜撰
#     - 不要新增虚构的平台或功能。
#     - 移除明显过时或无法修复的条目。
#
# # 输出格式 #
# 最终输出格式（JSON 代码块需置于最后，单独成段）：
# ```json
# {{
#   "<平台或应用名称>": {{
#     "<操作名称>": {{
#       "preconditions": "...",
#       "steps": "... -> ... -> ...",
#       "notes": "..."
#     }}
#   }}
# }}
# ```
# 注意：
# 你可以在 JSON 输出前加入任意长度的思考、总结或提炼内容。
# 但 JSON 代码块必须格式正确并独立输出，以便后续解析。
# """
merge_application_prompt = """\
# CONTEXT #
You are the **Application Operation Guide Merge Expert**.
Your responsibility is to **merge, deduplicate, normalize, and improve** a dictionary of "Platform/Application Operation Guides".

# INPUT #
- Current "Platform/Application Operation Guides":
<Platform/Application Operation Guides>
{guidance}
</Platform/Application Operation Guides>

# Objective #
- Identify and merge similar/duplicate operation steps.
- Normalize platform/application names into canonical forms.
- Improve unclear or low-quality steps to ensure concise, unambiguous, and reusable guides.

# Merge & Improvement Rules #
1. Platform Canonicalization
    - Merge aliases/variants of the same platform into a single, canonical platform name.
    - Example: `FastAPI Code Development` / `FastAPI Deployment` → `FastAPI`.
    - Use consistent casing and naming (e.g., GitLab, FastAPI, RocketChat).
2. Clustering by Operation Intent
    - Group entries by operation purpose.
    - Example: create/add/new → Create; start/run/launch → Start.
3. Consolidation
    - Keep the clearest, most general operation name.
    - Merge steps, remove redundancy, prefer reliable and safe versions.
4. Preconditions & Notes
    - Add `preconditions` at the start if required (e.g., dependencies installed, logged in).
    - Add `notes` if there are risks or cautions.
5. Clarity
    - Use precise actions. Example: use `Click "New Issue" Button` instead of `Click Button`, replace `parsing` with `direct observation extraction` or `Python-based parsing`.
6. Terminology & Style
    - Use a consistent imperative style: `Open -> Select -> Configure -> Save -> Verify`.
7. Do Not Invent
    - Do not add fake platforms or fake capabilities.
    - Remove entries that are clearly obsolete or unfixable.

# Output Format #
Final output format (JSON block must be placed last and occupy a separate paragraph):
```json
{{
  "<platform_or_application_name>": {{
    "<operation_name>": {{
      "preconditions": "...",
      "steps": "... -> ... -> ...",
      "notes": "..."
    }}
  }}
}}
```
Note:
You can include any length of thought, summary, or refinement before the JSON output.
However, the JSON block must be formatted correctly and output independently to facilitate subsequent parsing.
"""
