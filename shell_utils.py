"""
Linux/Shell 命令查询与执行工具模块。
封装 subprocess，提供统一的命令执行接口，可在测试或脚本中直接导入使用。
"""
from __future__ import annotations

import subprocess
import shlex
from typing import NamedTuple


class CommandResult(NamedTuple):
    """命令执行结果"""
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        """命令是否执行成功（返回码为 0）"""
        return self.returncode == 0


def run(cmd: str, timeout: int = 30, cwd: str | None = None, check: bool = False) -> CommandResult:
    """
    执行一条 Linux/shell 命令。

    参数:
        cmd: 要执行的完整命令字符串（如 "ls -la"、"grep -r 'foo' ."），
             会自动按 shell 语义分词。
        timeout: 超时秒数，默认 30。
        cwd: 工作目录，默认当前目录。
        check: 为 True 时，命令失败直接抛出 CalledProcessError；为 False 时返回结果让调用方自行判断。

    返回:
        CommandResult: 包含 returncode、stdout、stderr 三个字段，另有 ok 属性快捷判断成功与否。

    示例:
        >>> r = run("ls -la")
        >>> print(r.stdout)
        >>> if r.ok:
        ...     print("成功")
    """
    args = shlex.split(cmd)
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd,
    )
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)

    return CommandResult(
        returncode=proc.returncode,
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def run_pipe(*commands: str, timeout: int = 30, cwd: str | None = None) -> CommandResult:
    """
    执行管道命令链。每个字符串是一条命令，依次通过管道连接。

    示例:
        >>> r = run_pipe("echo 'hello\nworld'", "grep w")
        >>> print(r.stdout)  # world
    """
    procs = []
    prev_stdin = None
    for i, cmd in enumerate(commands):
        kwargs = dict(
            args=shlex.split(cmd),
            capture_output=True if i == len(commands) - 1 else False,
            text=True,
            cwd=cwd,
        )
        if i == 0 and prev_stdin is not None:
            kwargs["stdin"] = prev_stdin
        elif i > 0:
            kwargs["stdin"] = procs[-1].stdout
        procs.append(subprocess.Popen(**kwargs))
        if i > 0:
            procs[i - 1].stdout.close()

    stdout, stderr = procs[-1].communicate(timeout=timeout)
    returncode = procs[-1].returncode

    return CommandResult(
        returncode=returncode,
        stdout=stdout.strip() if stdout else "",
        stderr=stderr.strip() if stderr else "",
    )


def query(cmd: str, timeout: int = 30, cwd: str | None = None) -> str:
    """
    执行命令并以字符串返回 stdout（失败时返回空字符串）。

    适用于快速获取命令输出、当作"命令查询"使用。

    示例:
        >>> hostname = query("hostname")
        >>> lines = query("wc -l /etc/hosts")
    """
    result = run(cmd, timeout=timeout, cwd=cwd)
    return result.stdout


# ---- 以下为常用 Linux 查询快捷函数 ----


def which(program: str) -> str:
    """查程序是否在 PATH 中，返回路径；未找到返回空字符串。"""
    return query(f"which {program}")


def env_var(name: str) -> str:
    """获取环境变量值（通过 shell echo）。"""
    return query(f"echo ${name}")


def disk_usage(path: str = ".") -> str:
    """查看磁盘使用情况。"""
    return query(f"du -sh {path}")


def free_memory() -> str:
    """查看可用内存。"""
    return query("free -h")


def running_processes(keyword: str) -> str:
    """根据关键字查找正在运行的进程。"""
    return query(f"ps aux | grep {keyword}")
