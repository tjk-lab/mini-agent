from tools.registry import (
    TOOL_FUNCTIONS,
    TOOL_SCHEMAS,
)


def test_tool_functions_exist():
    expected_tools = {
        "calculator",
        "list_files",
        "read_file",
        "write_file",
    }

    assert set(TOOL_FUNCTIONS.keys()) == expected_tools


def test_tool_functions_are_callable():
    for tool_name, tool_function in TOOL_FUNCTIONS.items():
        assert callable(tool_function), (
            f"{tool_name} 对应的对象不是可调用函数"
        )


def test_tool_schemas_have_matching_functions():
    schema_names = {
        schema["name"]
        for schema in TOOL_SCHEMAS
    }

    function_names = set(TOOL_FUNCTIONS.keys())

    assert schema_names == function_names


def test_tool_schema_structure():
    for schema in TOOL_SCHEMAS:
        assert schema["type"] == "function"
        assert "name" in schema
        assert "description" in schema
        assert "parameters" in schema