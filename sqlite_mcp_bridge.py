#!/usr/bin/env python3
import sqlite3
import sys
import json

def query_db(db_path, query):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    db_path = sys.argv[1]
    # Basic MCP server logic here
