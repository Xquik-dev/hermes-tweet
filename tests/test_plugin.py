from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from typing import Any

from hermes_tweet import register


class DummyContext:
    def __init__(self) -> None:
        self.tools: list[dict[str, Any]] = []
        self.commands: list[dict[str, Any]] = []
        self.skills: list[tuple[str, Path]] = []

    def register_tool(self, **kwargs: Any) -> None:
        self.tools.append(kwargs)

    def register_command(self, name: str, **kwargs: Any) -> None:
        self.commands.append({"name": name, **kwargs})

    def register_skill(self, name: str, skill_md: Path) -> None:
        self.skills.append((name, skill_md))


def test_register_wires_tools_commands_and_skill() -> None:
    ctx = DummyContext()

    register(ctx)

    assert [tool["name"] for tool in ctx.tools] == [
        "tweet_explore",
        "tweet_read",
        "tweet_action",
    ]
    assert [command["name"] for command in ctx.commands] == ["xstatus", "xtrends"]
    assert ctx.skills == [
        (
            "hermes-tweet",
            Path(__file__).parents[1] / "hermes_tweet" / "skills" / "hermes-tweet" / "SKILL.md",
        )
    ]


def test_root_entrypoint_loads_as_hermes_directory_plugin() -> None:
    repo_root = Path(__file__).parents[1]
    previous_path = sys.path.copy()
    previous_hermes_tweet = sys.modules.pop("hermes_tweet", None)
    module_prefix = "hermes_plugins.hermes_tweet_probe"

    try:
        sys.path = [path for path in sys.path if Path(path or ".").resolve() != repo_root]

        parent = types.ModuleType("hermes_plugins")
        parent.__path__ = []
        parent.__package__ = "hermes_plugins"
        sys.modules["hermes_plugins"] = parent

        spec = importlib.util.spec_from_file_location(
            module_prefix,
            repo_root / "__init__.py",
            submodule_search_locations=[str(repo_root)],
        )
        assert spec is not None
        assert spec.loader is not None

        module = importlib.util.module_from_spec(spec)
        module.__package__ = module_prefix
        module.__path__ = [str(repo_root)]
        sys.modules[module_prefix] = module
        spec.loader.exec_module(module)

        assert callable(module.register)
    finally:
        sys.path = previous_path
        for module_name in list(sys.modules):
            if module_name == module_prefix or module_name.startswith(f"{module_prefix}."):
                del sys.modules[module_name]
        if previous_hermes_tweet is not None:
            sys.modules["hermes_tweet"] = previous_hermes_tweet
