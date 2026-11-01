import sys
from types import SimpleNamespace

from app import ask as ask_module


def test_ask_displays_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=34),
        text="回答",
    )

    class FakeClient:
        def __init__(self, api_key):
            self.models = SimpleNamespace(generate_content=lambda **kwargs: response)

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    assert "入力: 12 / 出力: 34" in capsys.readouterr().out


def test_interactive_asks_follow_up_questions_in_the_same_chat(
    monkeypatch, capsys
):
    class FakeChat:
        def __init__(self):
            self.questions = []

        def send_message(self, message):
            self.questions.append(message)
            return SimpleNamespace(
                usage_metadata=None,
                text=f"{message}への回答",
            )

    chat = FakeChat()
    created_chats = []

    class FakeClient:
        def __init__(self, api_key):
            self.chats = SimpleNamespace(
                create=lambda **kwargs: created_chats.append(kwargs) or chat
            )

    questions = iter(["最初の質問", "続けて質問", ""])
    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("builtins.input", lambda prompt: next(questions))
    monkeypatch.setattr(sys, "argv", ["app.ask", "--interactive"])

    ask_module.main()

    assert created_chats == [{"model": ask_module.MODEL}]
    assert chat.questions == ["最初の質問", "続けて質問"]
    output = capsys.readouterr().out
    assert "最初の質問への回答" in output
    assert "続けて質問への回答" in output