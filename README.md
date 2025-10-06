# Snowflake Simple MCP Server❄️

SnowflakeとClaudeを接続するシンプルなMCP（Model Context Protocol）サーバーです。

## 特徴

-  FastMCPを使用したシンプルな実装
-  セッション維持による認証の効率化
-  Snowflakeのクエリ実行とデータ取得
-  Claude Desktopとの統合

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/RyutoYoda/snowflake-simple-mcp-server.git
cd snowflake-simple-mcp-server
```

### 2. 仮想環境の作成とライブラリのインストール

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 環境変数の設定

```bash
cp sample.env .env
```

`.env` ファイルを編集して、Snowflakeの接続情報を設定してください：

```bash
SNOWSQL_ACCOUNT=your-account-name
SNOWSQL_USER=your-username
SNOWSQL_AUTHENTICATOR=externalbrowser
SNOWSQL_ROLE=your-role
```

### 4. Claude Desktopの設定

Claude Desktopの設定ファイルを編集します：

#### 設定ファイルの場所
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### 設定コマンド例（macOS）
```bash
# 設定ファイルを開く
open "~/Library/Application Support/Claude/claude_desktop_config.json"

# またはコマンドラインエディタで編集
nano "~/Library/Application Support/Claude/claude_desktop_config.json"
```

#### 設定内容
以下の内容を追加または編集してください：

```json
{
  "mcpServers": {
    "snowflake-simple": {
      "command": "/path/to/your/snowflake-simple-mcp-server/venv/bin/python",
      "args": ["/path/to/your/snowflake-simple-mcp-server/simple_fastmcp.py"]
    }
  }
}
```

**重要**: パスは実際のプロジェクトディレクトリに置き換えてください。

### 5. Claude Desktopの再起動

設定を反映するため、Claude Desktopを再起動してください。

## 利用可能なツール

- **test_connection**: MCPサーバーの動作確認
- **execute_query**: Snowflakeでのクエリ実行

## トラブルシューティング

### 認証エラー

- `.env` ファイルの設定を確認してください
- `externalbrowser` 認証の場合、初回接続時にブラウザが開きます
- セッション維持により、2回目以降は認証なしで接続できます

### 接続エラー

- Snowflakeアカウント名が正しいか確認してください
- ネットワーク接続を確認してください
- ログファイルでエラー詳細を確認してください

## 開発

### Makefileコマンド

```bash
# 利用可能なコマンドを表示
make help

# Snowflakeに直接接続
make connect

# 接続テスト（簡単なクエリを実行）
make test

# SnowSQLのバージョン確認
make version
```

### テスト実行

```bash
source venv/bin/activate
python simple_fastmcp.py
```

サーバーが正常に起動することを確認できます。
