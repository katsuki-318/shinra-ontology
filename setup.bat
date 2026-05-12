@echo off
echo ====================================
echo 神羅万象オントロジー セットアップ
echo ====================================
echo.

:: Python確認
python --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python が見つかりません
  echo  → https://python.org からインストールしてください
  pause
  exit /b 1
)
echo [OK] Python 確認

:: rdflib インストール
echo.
echo [installing] rdflib ...
pip install rdflib --quiet
echo [OK] rdflib インストール完了

:: バリデーション実行
echo.
echo === バリデーション実行 ===
python tests\validate.py
echo.

:: SPARQLサンプル実行
echo === SPARQLサンプル実行 ===
python tests\sparql_examples.py
echo.

echo ====================================
echo セットアップ完了
echo ====================================
echo.
echo 次のステップ:
echo   1. GitHub private repo を作成して git init / git remote add origin
echo   2. Protege 5.6+ で src\shinra-core.ttl を開いて可視化確認
echo   3. ROBOT https://github.com/ontodev/robot/releases から robot.jar を取得
echo      java -jar robot.jar reason --reasoner ELK --input src\shinra-core.ttl
echo   4. Oxigraph で SPARQL エンドポイントを立てる:
echo      oxigraph serve --location data/ --bind 0.0.0.0:7878
echo.
pause
