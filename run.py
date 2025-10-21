
import os
import asyncio
import argparse
import subprocess

from agent import MUSE
from prompt.system_prompt import MUSE_sys_prompt

"""
This Python script needs to be run in the TAC task container.
"""

# ===============================
# 该脚本的总体结构说明
# ===============================
# 1. 解析命令行参数，得到要执行的任务、模式、LLM 等基础配置。
# 2. 根据模式（训练 / 测试）初始化 MUSE 智能体，并运行用户指定的任务。
# 3. 任务运行结束后，调用 TAC 评测脚本获取评估结果，并写入输出目录。
# 4. 日志全部通过 AgentLogger 记录，便于在容器中查看执行过程。
#
# 这是 TAC 平台的入口脚本，因此在本文件中添加足够的中文注释，
# 便于理解各个步骤对应的逻辑与数据流转。

def get_tac_evaluation(task_name: str, agent_name: str, mode: str, round: int) -> str:
    """调用 TAC 提供的评测脚本, 返回包含检查点与评估信息的文本。"""

    # 组装评测脚本的执行命令。使用 python_default 解释器运行 /utils/eval.py,
    # 并传入智能体执行产生的历史轨迹与评测结果输出路径。
    cmd = [
        "python_default", "/utils/eval.py",
        "--trajectory_path", f"/MUSE/outputs/{agent_name}/{mode}/{task_name}/round_{round}/history.txt",
        "--result_path", f"/MUSE/outputs/{agent_name}/{mode}/{task_name}/round_{round}/agent_eval_output.json"
    ]

    # 环境变量中需要包含解密密钥, 同时保留原有的系统环境变量。
    env = {"DECRYPTION_KEY": "theagentcompany is all you need", **os.environ}

    # 使用 subprocess.run 同步调用评测脚本, capture_output=True 用于捕获标准输出与错误输出。
    proc = subprocess.run(cmd, capture_output=True, env=env, text=True, cwd="/workspace")

    # 评测脚本输出的内容是最终得分, 将 stdout 与 stderr 拼接方便排查问题。
    evaluation = proc.stdout + "\n" + proc.stderr

    # checkpoints.md 中包含任务执行过程需要展示的检查点信息。
    with open("/instruction/checkpoints.md", "r") as f:
        checkpoints = f.read()

    # 将检查点与评估结果包装成统一的 XML 样式文本, 便于后续日志展示。
    result = f"<checkpoints>\n{checkpoints}\n</checkpoints>\n<evaluation>\n{evaluation}\n<evaluation>\n"

    return result

async def main():
    """脚本主逻辑: 解析参数、运行智能体并拉取评测结果。"""

    # -------------------------
    # 解析命令行参数
    # -------------------------
    # 通过 argparse 提供默认参数, 便于本地调试。
    parser = argparse.ArgumentParser(description="Interact with Agent")
    parser.add_argument("--agent_name", type=str, help="Agent name", default="test_agent")
    parser.add_argument("--task_name", type=str, help="Task name", default="test_task")
    parser.add_argument("--task", type=str, help="Please enter your instructions")
    parser.add_argument("--mode", type=str, help="Training mode", default="test")
    parser.add_argument("--round", type=int, help="Training round", default=1)
    parser.add_argument("--llm", type=str, help="Base LLM", default="gemini-2.5-flash")
    args = parser.parse_args()

    mode = args.mode

    # -------------------------
    # 根据模式初始化智能体
    # -------------------------
    # 训练模式会启用记忆写入与更新, 测试模式则关闭记忆相关的 Side Effect。
    if mode == "train":
        agent = MUSE(
            init_model_name=args.llm,
            sys_prompt_template=MUSE_sys_prompt,
            memory_dir="memory",
            agent_name=args.agent_name,
            task_name=args.task_name,
            output_dir="outputs",
            mode_label="train",
            task_round=args.round,
            use_memory=True,
            update_memory=True,
            # lang="zh"
            # env_feedback_func=get_tac_evaluation,
            # env_feedback_args={"task_name": args.task_name, "agent_name": agent_name, "mode": args.mode, "round": args.round}
        )
        # 记录任务描述, subtitle/title 用于在日志 UI 中显示模块化结构。
        agent.logger.log_task(args.task, subtitle="STARTING······", title="Task")
        # 运行任务主体。subtask_action_limit 等参数定义智能体的推理预算。
        await agent.run(args.task, subtask_action_limit=20, num_actions_scale=8, time_limit=2400, verbose=False)
    else:
        agent = MUSE(
            init_model_name=args.llm,
            sys_prompt_template=MUSE_sys_prompt,
            memory_dir="memory",
            agent_name=args.agent_name,
            task_name=args.task_name,
            output_dir="outputs",
            mode_label="test",
            task_round=args.round,
            use_memory=False,
            update_memory=False,
            # lang="zh"
        )
        agent.logger.log_task(args.task, subtitle="STARTING······", title="Task")
        await agent.run(args.task, subtask_action_limit=20, num_actions_scale=8, time_limit=2400, verbose=False)

    # -------------------------
    # 触发评测并保存结果
    # -------------------------
    # 运行结束后, 将评测结果写入输出目录, 方便后续回放与比对。
    eval_log = get_tac_evaluation(args.task_name, args.agent_name, args.mode, args.round)
    agent.logger.log_task(eval_log, subtitle="TEST", title="Final Score")
    with open(agent._get_output_dir() / "eval_log.txt", mode="w") as f:
        f.write(eval_log)

if __name__ == "__main__":
    asyncio.run(main())
