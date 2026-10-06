from pathlib import Path


# 默认工作目录
WORKSPACE = Path("workspace")

# 默认输入目录
INPUT_DIR = WORKSPACE / "input"

# 默认输出目录
OUTPUT_DIR = WORKSPACE / "output"


def get_safe_path(base_dir: Path, filename: str) -> Path:
    """
    根据指定目录和文件名生成安全路径。

    这个函数会检查 filename 是否试图通过 ../
    跳出指定目录。
    """

    base_path = base_dir.resolve()
    file_path = (base_dir / filename).resolve()

    if not file_path.is_relative_to(base_path):
        raise PermissionError(
            f"禁止访问指定目录之外的路径：{filename}"
        )

    return file_path


def list_files(
    input_dir: Path = INPUT_DIR,
) -> list[str]:
    """
    列出输入目录中的所有文件。

    正常运行时默认读取 workspace/input。
    测试时可以传入其他临时目录。
    """

    input_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    files = []

    for path in input_dir.iterdir():
        if path.is_file():
            files.append(path.name)

    return files


def read_file(
    filename: str,
    input_dir: Path = INPUT_DIR,
) -> str:
    """
    读取输入目录中的指定文本文件。

    正常运行时默认读取 workspace/input。
    测试时可以传入其他临时目录。
    """

    file_path = get_safe_path(
        input_dir,
        filename,
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"输入文件不存在：{filename}"
        )

    return file_path.read_text(
        encoding="utf-8",
    )


def write_file(
    filename: str,
    content: str,
    output_dir: Path = OUTPUT_DIR,
) -> str:
    """
    把文本写入输出目录。

    正常运行时默认写入 workspace/output。
    测试时可以传入其他临时目录。
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = get_safe_path(
        output_dir,
        filename,
    )

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    # 保持和之前版本一致，
    # 避免已有测试和 Agent 行为发生变化
    return f"文件已写入 output/{filename}"