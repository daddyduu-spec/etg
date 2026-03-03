"""Test del protocollo di messaggistica ETG Studio."""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from protocols import ETGMessage, ETGSession, MessageStatus, MessageType, AgentRole


def test_message_roundtrip():
    """Verifica serializzazione/deserializzazione messaggi."""
    msg = ETGMessage(
        session_id="test-session-123",
        project_name="Test Project",
        sender=AgentRole.ORCHESTRATOR,
        recipient=AgentRole.GEMINI,
        msg_type=MessageType.TASK,
        subject="Test task",
        payload={"brief": "Costruisci un sistema di test"},
        etg_path="etg://shared/test",
    )

    json_str = msg.to_json()
    restored = ETGMessage.from_json(json_str)

    assert restored.session_id == msg.session_id
    assert restored.project_name == msg.project_name
    assert restored.sender == msg.sender
    assert restored.payload["brief"] == msg.payload["brief"]
    print("[OK] test_message_roundtrip")


def test_message_inbox():
    """Verifica salvataggio messaggio nella inbox."""
    with tempfile.TemporaryDirectory() as tmpdir:
        inbox = Path(tmpdir) / "inbox" / "gemini"
        inbox.mkdir(parents=True)

        msg = ETGMessage(
            session_id="abc-123",
            project_name="Inbox Test",
            sender=AgentRole.ORCHESTRATOR,
            recipient=AgentRole.GEMINI,
            msg_type=MessageType.TASK,
            subject="Test inbox",
        )

        filepath = msg.save_to_inbox(inbox)
        assert filepath.exists()

        restored = ETGMessage.from_file(filepath)
        assert restored.session_id == "abc-123"
        print("[OK] test_message_inbox")


def test_session_save_load():
    """Verifica salvataggio e caricamento sessione."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_path = Path(tmpdir) / "sessions"

        session = ETGSession(
            project_name="Sessione Test",
            description="Descrizione test",
        )
        session.save(sessions_path)

        session_file = sessions_path / f"session_{session.session_id[:8]}.json"
        assert session_file.exists()

        restored = ETGSession.from_json(session_file.read_text())
        assert restored.project_name == "Sessione Test"
        assert restored.session_id == session.session_id
        print("[OK] test_session_save_load")


def test_workflow_order():
    """Verifica l'ordine del workflow degli agenti."""
    order = [AgentRole.GEMINI, AgentRole.CLAUDE, AgentRole.CHATGPT]
    assert order[0] == "gemini"
    assert order[1] == "claude"
    assert order[2] == "chatgpt"
    print("[OK] test_workflow_order: Gemini -> Claude -> ChatGPT")


if __name__ == "__main__":
    print("ETG Studio - Test protocollo\n")
    test_message_roundtrip()
    test_message_inbox()
    test_session_save_load()
    test_workflow_order()
    print("\nTutti i test passati [OK]")
