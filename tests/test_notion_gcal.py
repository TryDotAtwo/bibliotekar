"""
Tests for Notion and Google Calendar integration stubs.

These tests verify that clients raise appropriate errors when not configured,
and that unimplemented methods raise NotImplementedError.
"""

import pytest
from datetime import datetime, timedelta

from bibliotekar.notion_integration import NotionClient, NotionConfig
from bibliotekar.gcal_integration import GCalClient, GCalConfig


def test_notion_client_initialization() -> None:
    # Missing credentials should raise RuntimeError
    with pytest.raises(RuntimeError):
        NotionClient(NotionConfig(api_key="", database_id=""))
    # Proper configuration should instantiate but methods remain unimplemented
    client = NotionClient(NotionConfig(api_key="dummy", database_id="db"))
    with pytest.raises(NotImplementedError):
        client.create_page("Title", "Content")
    with pytest.raises(NotImplementedError):
        client.update_page("page_id", "Content")
    with pytest.raises(NotImplementedError):
        client.search("query")


def test_gcal_client_initialization() -> None:
    # Missing credentials should raise RuntimeError
    with pytest.raises(RuntimeError):
        GCalClient(GCalConfig(credentials_json=""))
    # Proper configuration should instantiate but methods remain unimplemented
    client = GCalClient(GCalConfig(credentials_json="{}"))
    start = datetime.now()
    end = start + timedelta(hours=1)
    with pytest.raises(NotImplementedError):
        client.create_event("Event", start, end)
    with pytest.raises(NotImplementedError):
        client.list_events(start, end)
    with pytest.raises(NotImplementedError):
        client.delete_event("event_id")