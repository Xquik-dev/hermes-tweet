from __future__ import annotations

_METHOD_ENUM = ["GET", "POST", "PATCH", "PUT", "DELETE"]

TWEET_EXPLORE = {
    "name": "tweet_explore",
    "description": (
        "Search the bundled Xquik endpoint catalog. Use this before calling "
        "tweet_read or tweet_action. This tool does not make network calls."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Keyword search across endpoint paths, summaries, parameters, "
                    "and response shapes."
                ),
            },
            "category": {"type": "string", "description": "Endpoint category filter."},
            "method": {
                "type": "string",
                "enum": _METHOD_ENUM,
                "description": "HTTP method filter.",
            },
            "path": {"type": "string", "description": "Exact or partial /api/v1 path filter."},
            "free": {"type": "boolean", "description": "Filter free or paid endpoints."},
            "mpp": {"type": "boolean", "description": "Filter MPP eligible endpoints."},
            "include_actions": {
                "type": "boolean",
                "description": "Include write-like and private endpoints in catalog results.",
                "default": False,
            },
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "default": 25,
                "description": "Maximum endpoint descriptors to return.",
            },
        },
        "additionalProperties": False,
    },
}

TWEET_READ = {
    "name": "tweet_read",
    "description": (
        "Invoke one catalog-listed read-only Xquik endpoint. Use concrete /api/v1 paths "
        "from tweet_explore. This tool rejects write-like and private endpoints."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "minLength": 8,
                "pattern": "^/api/v1/",
                "description": "Concrete /api/v1/... endpoint path.",
            },
            "query": {
                "type": "object",
                "description": "Query parameters as string, number, or boolean values.",
                "additionalProperties": {"type": ["string", "number", "boolean"]},
            },
        },
        "required": ["path"],
        "additionalProperties": False,
    },
}

TWEET_ACTION = {
    "name": "tweet_action",
    "description": (
        "Invoke one catalog-listed Xquik action endpoint, including writes and private reads. "
        "Disabled unless HERMES_TWEET_ENABLE_ACTIONS=true. Show the endpoint and payload "
        "to the user first."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "minLength": 8,
                "pattern": "^/api/v1/",
                "description": "Concrete /api/v1/... endpoint path.",
            },
            "method": {"type": "string", "enum": _METHOD_ENUM, "default": "POST"},
            "query": {
                "type": "object",
                "description": "Query parameters as string, number, or boolean values.",
                "additionalProperties": {"type": ["string", "number", "boolean"]},
            },
            "body": {
                "description": "JSON request body.",
                "type": ["object", "array", "string", "number", "boolean", "null"],
            },
            "reason": {
                "type": "string",
                "minLength": 1,
                "pattern": "\\S",
                "description": "Brief user-visible reason for the action.",
            },
        },
        "required": ["path", "reason"],
        "additionalProperties": False,
    },
}
