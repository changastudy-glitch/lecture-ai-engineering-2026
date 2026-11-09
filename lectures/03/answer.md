# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：エージェントの回答のほうが求めている回答形式を反映しており、正確な出力であった。
- `--trace` で見えたツール呼び出し（ツール名と引数）：[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": 
 search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition"
- 1つの質問での LLM 呼び出し回数（`requests`）：２回
- 追加したツールと、docstring に書いた説明：make_quiz
                                         """指定した回の用語から１つ選び、確認問題と答えを返す。

    「第3回の確認問題を出して」のように、復習用の問題を求められたときに使う。

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
