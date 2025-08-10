# 今日一番熱い株（無料MVP）

前日提出の**公式開示/規制資料/報道**から“注目トップ5”を生成し、**理由1文（80字）＋出典リンク**を配信する最小構成。

## 使い方（ローカル）
```bash
pip install fastapi uvicorn pandas
uvicorn app.main:app --reload
# -> http://127.0.0.1:8000/v1/highlights?date=2025-08-08&market=JP
# -> http://127.0.0.1:8000/v1/highlights?date=2025-08-08&market=US
```

## 構成
- `data/tags.csv` … タグ辞書（重み/キーワード）
- `data/templates.json` … 80字テンプレ
- `sample_output/` … サンプルJSON
- `app/reason.py` … タグ付け・要約生成の素地
- `app/main.py` … APIエンドポイント（サンプル読み出し）

## 重要
- ニュース本文は転載不可。**自作要約＋出典リンク**に徹してください。
- 本MVPは**価格データの再配信を行いません**。
- 本情報は投資助言ではありません。

