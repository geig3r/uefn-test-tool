"""Concrete callable actions behind the UEFN Test Tool menu."""


def log_environment() -> None:
    import unreal
    import uefn_test_tool

    unreal.log(str(uefn_test_tool.describe_environment()))


def reload_package() -> None:
    import importlib
    import uefn_test_tool

    importlib.reload(uefn_test_tool)
    uefn_test_tool.register()
