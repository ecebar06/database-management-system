# Mini Database Management System

A custom, lightweight, file-based database engine implemented in Python from scratch without relying on external SQL libraries or third-party database tools.

## Features

- **SQL-like Command Parser:** Parses and executes database commands including CREATE_TABLE, INSERT, SELECT, UPDATE, DELETE, and COUNT.
- **Relational Operations & Joins:** Implements inner JOIN logic to combine matching records across multiple tables based on key columns.
- **Conditional Querying:** Supports WHERE filtering with key-value condition pairs for selective data retrieval and modification.
- **Data Integrity & Validation:** Includes custom error handling for table/column existence checks and data type mismatches.
- **Custom Terminal Formatter:** Formats query outputs into ASCII tables with dynamic column width adjustments.

## Commands Supported

- CREATE_TABLE <table_name> <col1,col2,...>
- INSERT <table_name> <val1,val2,...>
- SELECT <table_name> <cols> WHERE {col:val}
- UPDATE <table_name> {col:new_val} WHERE {col:val}
- DELETE <table_name> WHERE {col:val}
- JOIN <table1,table2> ON <column>
- COUNT <table_name> WHERE {col:val}

## Tech Stack

- **Language:** Python 3.x
- **Core Libraries:** Standard Library (sys, os)

## How to Run

Execute the engine with an input command file:
python database.py input_commands.txt
