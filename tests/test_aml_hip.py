"""
Tests for AML‑HIP message formatting and validation.
"""

import bibliotekar.aml_hip as ah


def test_validate_message_no_pronouns():
    msg = "СУЩНОСТЬ:\nentity_id=1; type=test; state=ok\n"
    valid, errors = ah.validate_message(msg)
    assert valid, f"No errors expected, got {errors}"


def test_validate_message_detect_pronoun():
    msg = "СУЩНОСТЬ:\nentity_id=1; type=test; state=it is bad\n"
    valid, errors = ah.validate_message(msg)
    assert not valid
    assert any("pronoun" in e for e in errors)


def test_validate_message_missing_relation():
    msg = "СУЩНОСТЬ:\nentity_id 1 type test\n"
    valid, errors = ah.validate_message(msg)
    assert not valid
    assert any("lacks key=value" in e for e in errors)