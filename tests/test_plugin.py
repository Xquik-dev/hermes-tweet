from __future__ import annotations

import importlib.util
import inspect
import re
import sys
import types
from pathlib import Path
from typing import Any

from hermes_tweet import register
from hermes_tweet.tools import action_enabled, check_api_available


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


def test_register_keeps_official_hermes_plugin_gates_aligned() -> None:
    ctx = DummyContext()

    register(ctx)

    tools = {tool["name"]: tool for tool in ctx.tools}
    explore = tools["tweet_explore"]
    read = tools["tweet_read"]
    action = tools["tweet_action"]
    nonblank_property_names = {"minLength": 1, "pattern": "\\S"}

    assert "check_fn" not in explore
    assert "requires_env" not in explore
    assert explore["schema"]["name"] == "tweet_explore"
    assert explore["is_async"] is False
    explore_parameters = explore["schema"]["parameters"]
    for filter_name in ("query", "category", "path"):
        assert explore_parameters["properties"][filter_name]["minLength"] == 1
        assert explore_parameters["properties"][filter_name]["pattern"] == "\\S"

    assert read["check_fn"] is check_api_available
    assert read["requires_env"] == ["XQUIK_API_KEY"]
    assert read["schema"]["name"] == "tweet_read"
    assert read["is_async"] is False
    read_parameters = read["schema"]["parameters"]
    assert read_parameters["properties"]["path"]["minLength"] == len("/api/v1/")
    assert read_parameters["properties"]["path"]["pattern"] == (
        "^(?:/api/v1/|https?://[^/]+/api/v1/)"
    )
    assert "copied API URL" in read_parameters["properties"]["path"]["description"]
    assert read_parameters["properties"]["query"]["propertyNames"] == nonblank_property_names

    assert action["check_fn"] is action_enabled
    assert action["requires_env"] == ["XQUIK_API_KEY", "HERMES_TWEET_ENABLE_ACTIONS"]
    assert action["schema"]["name"] == "tweet_action"
    assert action["is_async"] is False
    action_parameters = action["schema"]["parameters"]
    assert action_parameters["required"] == ["path", "reason"]
    assert action_parameters["properties"]["path"]["minLength"] == len("/api/v1/")
    assert action_parameters["properties"]["path"]["pattern"] == (
        "^(?:/api/v1/|https?://[^/]+/api/v1/)"
    )
    assert "copied API URL" in action_parameters["properties"]["path"]["description"]
    assert action_parameters["properties"]["query"]["propertyNames"] == nonblank_property_names
    assert action_parameters["properties"]["method"]["default"] == "POST"
    assert action_parameters["properties"]["reason"]["minLength"] == 1
    assert action_parameters["properties"]["reason"]["pattern"] == "\\S"


def test_registered_path_schema_allows_only_api_paths_and_urls() -> None:
    ctx = DummyContext()

    register(ctx)

    tools = {tool["name"]: tool for tool in ctx.tools}
    for tool_name in ("tweet_read", "tweet_action"):
        path_schema = tools[tool_name]["schema"]["parameters"]["properties"]["path"]
        pattern = re.compile(path_schema["pattern"])

        assert pattern.search("/api/v1/account") is not None
        assert pattern.search("https://xquik.com/api/v1/account") is not None
        assert pattern.search("https://xquik.com/not-api/account") is None
        assert pattern.search("/not-api/account") is None


def test_registered_tool_handlers_accept_future_hermes_context_kwargs() -> None:
    ctx = DummyContext()

    register(ctx)

    for tool in ctx.tools:
        parameters = inspect.signature(tool["handler"]).parameters.values()
        assert any(parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in parameters)


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
