#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrates the flat CSV files to an SQLite database with FTS5 full-text search.
This improves querying speed, enables relational joins, and simplifies the codebase.
"""
import sqlite3
import csv
from core import CSV_CONFIG, STACK_CONFIG, DATA_DIR

DB_PATH = DATA_DIR / "ui_ux_knowledge.db"

def sanitize_col_name(col):
    return col.replace(" ", "_").replace("/", "_").replace("&", "and").replace("(", "").replace(")", "").replace("-", "_").replace("'", "").lower()

def init_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # We will create a general FTS5 table for all domains to enable cross-domain search easily,
    # and individual tables for structured querying.
    cursor.execute('''
        CREATE VIRTUAL TABLE search_index USING fts5(
            domain,
            name,
            keywords,
            content,
            table_name UNINDEXED,
            record_id UNINDEXED
        )
    ''')

    # Domain Tables
    for domain, config in CSV_CONFIG.items():
        table_name = f"domain_{domain.replace('-', '_')}"
        cols = [sanitize_col_name(col) for col in config["output_cols"]]
        
        create_stmt = f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, "
        create_stmt += ", ".join([f'"{col}" TEXT' for col in cols])
        create_stmt += ")"
        cursor.execute(create_stmt)

    # Stack Tables
    for stack, config in STACK_CONFIG.items():
        table_name = f"stack_{stack.replace('-', '_')}"
        # We know _STACK_COLS from core.py
        stack_cols = ["category", "guideline", "description", "do", "dont", "code_good", "code_bad", "severity", "docs_url", "dark_mode_strategy", "ai_integration_level", "privacy_tier", "agent_readiness", "performance_budget"]
        cols = [sanitize_col_name(col) for col in stack_cols]
        
        create_stmt = f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, "
        create_stmt += ", ".join([f'"{col}" TEXT' for col in cols])
        create_stmt += ")"
        cursor.execute(create_stmt)
    
    conn.commit()
    return conn

def migrate_data(conn):
    cursor = conn.cursor()
    
    # Migrate Domains
    print("Migrating domain CSVs to SQLite...")
    for domain, config in CSV_CONFIG.items():
        csv_file = DATA_DIR / config["file"]
        if not csv_file.exists():
            print(f"Skipping {csv_file}, doesn't exist.")
            continue
            
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            table_name = f"domain_{domain.replace('-', '_')}"
            
            for row in reader:
                # Insert into structured table
                ordered_values = []
                for col in config["output_cols"]:
                    ordered_values.append(row.get(col, ""))
                
                placeholders = ", ".join(["?"] * len(ordered_values))
                cols_quoted = [f'"{sanitize_col_name(c)}"' for c in config['output_cols']]
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(cols_quoted)}) VALUES ({placeholders})", ordered_values)
                record_id = cursor.lastrowid
                
                # Insert into FTS5 index
                search_content = " ".join([str(row.get(col, "")) for col in config["search_cols"]])
                
                # Try to extract a primary name/title depending on domain
                name_col = config["output_cols"][0] # Usually the first column is the name/category
                
                cursor.execute("INSERT INTO search_index (domain, name, keywords, content, table_name, record_id) VALUES (?, ?, ?, ?, ?, ?)", 
                               (domain, row.get(name_col, ""), row.get("Keywords", ""), search_content, table_name, record_id))
                
    # Migrate Stacks
    print("Migrating stack CSVs to SQLite...")
    stack_cols = ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL", "Dark_Mode_Strategy", "AI_Integration_Level", "Privacy_Tier", "Agent_Readiness", "Performance_Budget"]
    
    for stack, config in STACK_CONFIG.items():
        csv_file = DATA_DIR / config["file"]
        if not csv_file.exists():
            print(f"Skipping {csv_file}, doesn't exist.")
            continue
            
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            table_name = f"stack_{stack.replace('-', '_')}"
            cols_sanitized = [f'"{sanitize_col_name(c)}"' for c in stack_cols]
            
            for row in reader:
                ordered_values = [row.get(col, "") for col in stack_cols]
                placeholders = ", ".join(["?"] * len(ordered_values))
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(cols_sanitized)}) VALUES ({placeholders})", ordered_values)
                record_id = cursor.lastrowid
                
                search_content = f"{row.get('Category', '')} {row.get('Guideline', '')} {row.get('Description', '')}"
                cursor.execute("INSERT INTO search_index (domain, name, keywords, content, table_name, record_id) VALUES (?, ?, ?, ?, ?, ?)", 
                               (f"stack_{stack}", row.get('Guideline', ''), "", search_content, table_name, record_id))
    
    conn.commit()
    print(f"Migration complete. Database saved to {DB_PATH}")

if __name__ == "__main__":
    conn = init_db()
    migrate_data(conn)
    conn.close()
