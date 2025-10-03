#!/usr/bin/env python3
from fastmcp import FastMCP
import snowflake.connector
import os
import json
from dotenv import load_dotenv
import atexit

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Simple Snowflake Server")

# Snowflake configuration
SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWSQL_ACCOUNT"),
    "user": os.getenv("SNOWSQL_USER"),
    "authenticator": os.getenv("SNOWSQL_AUTHENTICATOR", "externalbrowser"),
    "role": os.getenv("SNOWSQL_ROLE"),
    "warehouse": os.getenv("SNOWSQL_WAREHOUSE"),
    "database": os.getenv("SNOWSQL_DATABASE"),
    "schema": os.getenv("SNOWSQL_SCHEMA"),
    "client_session_keep_alive": True,  # Keep session alive
}

# Global connection pool
_connection = None

def get_connection():
    """Get or create a Snowflake connection"""
    global _connection
    
    if _connection is None or _connection.is_closed():
        config = {k: v for k, v in SNOWFLAKE_CONFIG.items() if v is not None}
        
        # Check required fields
        if not config.get("account"):
            raise ValueError("SNOWSQL_ACCOUNT environment variable is required")
        if not config.get("user"):
            raise ValueError("SNOWSQL_USER environment variable is required")
        
        _connection = snowflake.connector.connect(**config)
    
    return _connection

def cleanup_connection():
    """Clean up the connection on exit"""
    global _connection
    if _connection and not _connection.is_closed():
        _connection.close()

# Register cleanup function
atexit.register(cleanup_connection)

@mcp.tool()
def test_connection() -> str:
    """Test if the MCP server is working"""
    return "MCP server is working!"

@mcp.tool()
def execute_query(query: str) -> str:
    """
    Execute a SQL query on Snowflake
    
    Args:
        query: SQL query to execute
        
    Returns:
        Query result as JSON string
    """
    cursor = None
    try:
        # Get or reuse connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Execute query
        cursor.execute(query)
        
        # Get results
        if cursor.description:
            # Query returned results
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            result = {
                "success": True,
                "columns": columns,
                "data": rows,
                "row_count": len(rows)
            }
        else:
            # Query was an action (like USE DATABASE)
            result = {
                "success": True,
                "message": f"Query executed successfully: {query}",
                "rows_affected": cursor.rowcount
            }
        
        return json.dumps(result, indent=2, default=str)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "query": query
        }, indent=2)
    finally:
        if cursor:
            cursor.close()
        # Don't close the connection - keep it alive for reuse

if __name__ == "__main__":
    mcp.run(transport="stdio")