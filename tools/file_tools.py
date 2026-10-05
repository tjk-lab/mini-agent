from pathlib import Path


# workspace 根目录
WORKSPACE = Path("workspace")

# 用户提供的输入材料，只允许读取
INPUT_DIR = WORKSPACE / "input"

# Agent 生成的结果，只允许写入
OUTPUT_DIR = WORKSPACE / "output"


def get_safe_path(base_dir: Path, filename: str) -> Path:
    """
    根据指定目录和文件名生成安全路径。

    base_dir 可能是：
    - workspace/input
    - workspace/output

    这个函数负责检查 filename 有没有通过 ../ 跑到目录外面。
    """

    # 把基础目录转换成真实绝对路径
    base_path = base_dir.resolve()

    # 拼出最终文件路径，再转换成真实绝对路径
    file_path = (base_dir / filename).resolve()

    # 检查最终路径是否仍然属于 base_dir
    if not file_path.is_relative_to(base_path):
        raise PermissionError(
            f"禁止访问指定目录之外的路径：{filename}"
        )

    return file_path


def list_files() -> list[str]:
    """
    列出 input 目录中的所有文件。
    """

    # 如果 input 目录不存在，就创建
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = []

    for path in INPUT_DIR.iterdir():
        if path.is_file():
            files.append(path.name)

    return files


def read_file(filename: str) -> str:
    """
    只允许读取 workspace/input 中的文件。
    """

    file_path = get_safe_path(INPUT_DIR, filename)

    if not file_path.exists():
        raise FileNotFoundError(f"输入文件不存在：{filename}")

    return file_path.read_text(encoding="utf-8")


def write_file(filename: str, content: str) -> str:
    """
    只允许写入 workspace/output。
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_path = get_safe_path(OUTPUT_DIR, filename)

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    return f"文件已写入 output/{filename}"