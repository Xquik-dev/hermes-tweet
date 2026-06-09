from __future__ import annotations

from hermes_tweet.catalog import (
    Endpoint,
    explore,
    find_endpoint,
    matches_path,
    normalize_limit,
    normalize_method,
)


def test_matches_openapi_path_parameters() -> None:
    assert matches_path("/api/v1/x/tweets/{id}", "/api/v1/x/tweets/123") is True
    assert matches_path("/api/v1/x/tweets/:id", "/api/v1/x/tweets/123") is True
    assert matches_path("/api/v1/x/tweets/{id}/extra", "/api/v1/x/tweets//extra") is False
    assert matches_path("/api/v1/x/tweets/:id/extra", "/api/v1/x/tweets//extra") is False
    assert matches_path("/api/v1/x/tweets/{id}", "/api/v1/x/tweets/") is False
    assert matches_path("/api/v1/x/tweets/{id}", "/api/v1/x/tweets/123/extra") is False
    assert matches_path("/api/v1/x/tweets/{id}", "/api/v1/x/users/123") is False
    assert matches_path("/api/v1/x/tweets/{id}", "/api/v1/x/tweets") is False


def test_catalog_contains_tweet_search() -> None:
    endpoint = find_endpoint("GET", "/api/v1/x/tweets/search")
    assert endpoint is not None
    assert endpoint.action is False
    assert find_endpoint("GET", "/api/v1/missing") is None


def test_catalog_excludes_api_key_admin() -> None:
    assert find_endpoint("POST", "/api/v1/api-keys") is None


def test_explore_hides_actions_by_default() -> None:
    results = explore({"query": "post tweet", "limit": 100})
    assert all(item["action"] is False for item in results)


def test_explore_parses_string_boolean_filters() -> None:
    hidden_actions = explore({"include_actions": "false", "query": "compose", "limit": 100})
    visible_actions = explore({"include_actions": "true", "query": "compose", "limit": 100})
    paid = explore({"free": "false", "include_actions": "true", "limit": 100})
    mpp_disabled = explore({"include_actions": "true", "limit": 100, "mpp": "false"})

    assert all(item["action"] is False for item in hidden_actions)
    assert any(item["action"] is True for item in visible_actions)
    assert paid
    assert all(item["free"] is False for item in paid)
    assert mpp_disabled
    assert all("mpp" not in item for item in mpp_disabled)


def test_explore_ignores_unknown_boolean_filter_strings() -> None:
    unfiltered = explore({"category": "tweets", "include_actions": True, "limit": 100})
    unknown_free = explore(
        {
            "category": "tweets",
            "free": "maybe",
            "include_actions": True,
            "limit": 100,
        }
    )

    assert unknown_free == unfiltered


def test_explore_ignores_malformed_optional_text_filters() -> None:
    unfiltered = explore({"include_actions": True, "limit": 100})
    malformed = explore(
        {
            "category": 123,
            "include_actions": True,
            "limit": 100,
            "method": True,
            "path": False,
            "query": [],
        }
    )
    blank_method = explore({"include_actions": True, "limit": 100, "method": "  "})

    assert malformed == unfiltered
    assert blank_method == unfiltered


def test_explore_filters_catalog() -> None:
    results = explore(
        {
            "category": "tweets",
            "free": False,
            "include_actions": True,
            "method": "GET",
            "mpp": True,
            "path": "/api/v1/x/tweets/search",
            "query": "search",
        }
    )

    assert results
    assert results[0]["path"] == "/api/v1/x/tweets/search"


def test_normalizers() -> None:
    truthy_limit = True
    falsey_limit = False

    assert normalize_method(None) == "GET"
    assert normalize_method("post") == "POST"
    assert normalize_method(" post ") == "POST"
    assert normalize_method("") == "GET"
    assert normalize_method(123) == "GET"
    assert normalize_method(None, default="POST") == "POST"
    assert normalize_limit(None) == 25
    assert normalize_limit(truthy_limit) == 25
    assert normalize_limit(falsey_limit) == 25
    assert normalize_limit(0) == 1
    assert normalize_limit("0") == 1
    assert normalize_limit(" 7 ") == 7
    assert normalize_limit(101) == 100
    assert normalize_limit("101") == 100
    assert normalize_limit(7) == 7
    assert normalize_limit("seven") == 25


def test_endpoint_to_dict_includes_optional_fields() -> None:
    endpoint = Endpoint(
        action=True,
        category="tweets",
        free=False,
        method="GET",
        mpp={"intent": "charge", "price": "$0.00015/call"},
        parameters=({"name": "q", "in": "query", "required": True, "type": "string"},),
        path="/api/v1/x/tweets/search",
        response_shape="OK",
        summary="Search tweets",
    )

    assert endpoint.to_dict() == {
        "action": True,
        "category": "tweets",
        "free": False,
        "method": "GET",
        "mpp": {"intent": "charge", "price": "$0.00015/call"},
        "parameters": [{"name": "q", "in": "query", "required": True, "type": "string"}],
        "path": "/api/v1/x/tweets/search",
        "responseShape": "OK",
        "summary": "Search tweets",
    }
