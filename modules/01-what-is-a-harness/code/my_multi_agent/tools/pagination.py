"""
Defines the decorator for paginated-read tools
"""

import json
import hashlib
import functools
from dataclasses import dataclass, field
from inspect import signature, Parameter
from typing import Callable, Mapping

from google.adk.tools import ToolContext


LISTINGS_KEY = "listings" # TODO: to be shifted to commons/session_state.py
MAX_LISTINGS_PER_TOOL = 5
FINAL_PAGE = "this is the final page"

@dataclass(frozen=True)
class Page:
    entries: list[dict]
    filters: dict
    next_page: int | None
    status: str = "ok"
    detail: str = ""
    extra: dict = field(default_factory=dict)   # anything else the tool wants to add


def _listing_key(filters: dict, page_size: int) -> str:
    """Short, stable id for one listing: the filters that were applied, plus the page size."""
    applied = {name: value for name, value in filters.items() if value is not None}
    text = json.dumps({"filters": applied, "page_size": page_size},
                      sort_keys=True, separators=(",", ":"))
    return hashlib.blake2b(text.encode(), digest_size=6).hexdigest()

def listings_section(tools: list) -> Callable[[Mapping], str]:
    """
    Build the part of an agent's instruction that says how far each listing of
    its own tools has been read.

    Returns a function of the session state. It gives an empty string when
    none of these tools has a recorded listing, so nothing is added then.
    The decorator below writes the records; this is their only reader.
    """
    tool_names = [tool.__name__ for tool in tools]

    def describe(state: Mapping) -> str:
        listings = state.get(LISTINGS_KEY) or {}
        lines = [
            f"- {tool_name}, filters {json.dumps(record['filters'], sort_keys=True)}: next_page is {record['next_page']}"
            for tool_name in tool_names
            for record in listings.get(tool_name, {}).values()
        ]
        if not lines:
            return ""
        return "\n".join([
            "# Listings already read in this conversation",
            "To continue one, call the same tool with the same filters and the next_page shown.",
            *lines,
        ])

    return describe


def pagination_decorator(tool_func):
    """
    Turn a tool that reads one page into a paginated-read tool.

    The tool declares `page` and `page_size` and returns a `Page`. This wrapper
    supplies `page_size` from session state, so the model never sees or sets it,
    hands the model a plain dict, and records in session state how far each
    listing has been read.

    A listing is one tool called with one set of filters. Example, with two
    wrapped tools and a page size of 20, after these calls:

        _list_employee_names(page=2)
        _find_employee(name="Garcia", page=1)      # more matches remain
        _find_employee(name="smith", page=1)       # all matches fit on one page

    session state holds:

        "listings": {
            "_list_employee_names": {
                "14a90c80ee97": {"filters": {}, "next_page": 3},
            },
            "_find_employee": {
                "51aeedc725e5": {"filters": {"name": "garcia"}, "next_page": 2},
                "821fe14899ac": {"filters": {"name": "smith"},
                                 "next_page": "this is the final page"},
            },
        }

    When the user asks for "the next page" in a later turn, the agent reads from
    this which page comes next for which filters. It does not have to remember.

    Rules:
    - The inner key is `_listing_key(filters, page_size)`. It is for code only.
    - Only `filters` and `next_page` are stored, never the entries.
    - A record reflects the most recent call for those filters.
    - Each tool keeps its MAX_LISTINGS_PER_TOOL most recent listings.
    - A missing next page is worded as FINAL_PAGE, the same in every tool.
    - A page below 1 is rejected before the tool runs.
    - A tool that returns anything other than a `Page`, such as its own failure
      dict, is passed through untouched and nothing is recorded.
    """
    tool_name = tool_func.__name__
    tool_func_signature = signature(tool_func)
    tool_wants_context = "tool_context" in tool_func_signature.parameters

    @functools.wraps(tool_func)
    def pagination_wrapper(*args, tool_context: ToolContext, **kwargs):
        if kwargs.get("page", 1) < 1:
            return {"status": "fail", "detail": "page must be 1 or higher, retry this tool call."}

        page_size = tool_context.state["read_page_size"]
        if tool_wants_context:
            kwargs["tool_context"] = tool_context    # hand it on only to a tool that declares it
        tool_result = tool_func(*args, page_size=page_size, **kwargs)

        if not isinstance(tool_result, Page):
            return tool_result          # the tool reported its own failure: pass it through

        next_page = tool_result.next_page if tool_result.next_page is not None else FINAL_PAGE
        record = {"filters": tool_result.filters, "next_page": next_page}

        # get currently stored listings in the session state
        listings = dict(tool_context.state.get(LISTINGS_KEY, {}))
        
        # get listings of this tool
        of_this_tool = dict(listings.get(tool_name, {}))

        # create key and store the currently fetched results of the tool call
        key = _listing_key(tool_result.filters, page_size)
        of_this_tool.pop(key, None)            # re-insert, so the most recent listing is last
        of_this_tool[key] = record
        
        # cache full --> invalidate the oldest entry
        for oldest in list(of_this_tool)[:-MAX_LISTINGS_PER_TOOL]:
            del of_this_tool[oldest]

        # store back into the session state
        listings[tool_name] = of_this_tool
        tool_context.state[LISTINGS_KEY] = listings    # assign the whole value: ADK saves on assignment

        # the model receives a plain dict: the Page's fields, with next_page worded, plus the tool's extras
        return {
            "status": tool_result.status,
            "detail": tool_result.detail,
            "entries": tool_result.entries,
            "filters": tool_result.filters,
            "next_page": next_page,
            **tool_result.extra,
        }

    # through this code, ADK shows the model and injects: the tool's own parameters, minus page_size
    #  - because page_size isnt supposed to be set by the model and if not removed it will think
    #     that it is its responsibility
    # (the wrapper supplies it), plus tool_context (the wrapper needs it even if the tool does not).
    parameters = [p for name, p in tool_func_signature.parameters.items() if name != "page_size"]
    if not tool_wants_context:
        parameters.append(Parameter(
            "tool_context", Parameter.KEYWORD_ONLY, annotation=ToolContext))
    pagination_wrapper.__signature__ = tool_func_signature.replace(parameters=parameters)
    return pagination_wrapper
