"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --interactive "LoRAとは何ですか？" # 会話履歴を保って続けて質問する

通常モードはツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
--interactive では同じ会話履歴を保って続けて質問できる。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai.chats import Chat
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def _print_usage(response: genai.types.GenerateContentResponse) -> None:
    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[トークン数] 入力: {usage.prompt_token_count} / "
            f"出力: {usage.candidates_token_count}"
        )


def ask(question: str, *, chat: Chat | None = None) -> str:
    if chat is None:
        client = genai.Client(api_key=get_api_key())
        response = client.models.generate_content(model=MODEL, contents=question)
    else:
        response = chat.send_message(question)

    _print_usage(response)
    return response.text


def _ask_interactively() -> None:
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)
    print("会話を始めます。終了するには空の質問を入力してください。")

    while True:
        try:
            question = input("[質問] ")
        except EOFError:
            print()
            return

        if not question.strip():
            return

        print(ask(question, chat=chat))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="会話履歴を保って続けて質問する",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.interactive:
            if args.question is not None:
                parser.error("質問を指定せずに --interactive を使ってください")
            _ask_interactively()
        else:
            question = args.question if args.question is not None else DEFAULT_QUESTION
            print(f"[質問] {question}\n")
            print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
