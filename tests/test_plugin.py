from __future__ import annotations

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
