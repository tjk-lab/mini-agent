import pytest

from tools.file_tools import (
    get_safe_path,
    list_files,
    read_file,
    write_file,
)


def test_safe_input_path(tmp_path):
    input_dir = tmp_path / "input"

    path = get_safe_path(
        input_dir,
        "a.txt",
    )

    assert path.is_relative_to(input_dir.resolve())


def test_safe_output_path(tmp_path):
    output_dir = tmp_path / "output"

    path = get_safe_path(
        output_dir,
        "summary.txt",
    )

    assert path.is_relative_to(output_dir.resolve())


def test_block_path_traversal(tmp_path):
    input_dir = tmp_path / "input"

    with pytest.raises(PermissionError):
        get_safe_path(
            input_dir,
            "../danger.txt",
        )


def test_list_files(tmp_path):
    input_dir = tmp_path / "input"

    input_dir.mkdir()

    (input_dir / "a.txt").write_text(
        "hello",
        encoding="utf-8",
    )

    (input_dir / "b.txt").write_text(
        "world",
        encoding="utf-8",
    )

    files = list_files(
        input_dir=input_dir,
    )

    assert sorted(files) == [
        "a.txt",
        "b.txt",
    ]


def test_read_file(tmp_path):
    input_dir = tmp_path / "input"

    input_dir.mkdir()

    test_file = input_dir / "a.txt"

    test_file.write_text(
        "hello from pytest",
        encoding="utf-8",
    )

    content = read_file(
        "a.txt",
        input_dir=input_dir,
    )

    assert content == "hello from pytest"


def test_read_missing_file(tmp_path):
    input_dir = tmp_path / "input"

    input_dir.mkdir()

    with pytest.raises(FileNotFoundError):
        read_file(
            "missing.txt",
            input_dir=input_dir,
        )


def test_write_file(tmp_path):
    output_dir = tmp_path / "output"

    result = write_file(
        "test_output.txt",
        "hello from pytest",
        output_dir=output_dir,
    )

    assert result == "文件已写入 output/test_output.txt"

    output_file = output_dir / "test_output.txt"

    assert output_file.exists()

    assert (
        output_file.read_text(
            encoding="utf-8",
        )
        == "hello from pytest"
    )


def test_write_file_blocks_path_traversal(tmp_path):
    output_dir = tmp_path / "output"

    with pytest.raises(PermissionError):
        write_file(
            "../danger.txt",
            "danger",
            output_dir=output_dir,
        )