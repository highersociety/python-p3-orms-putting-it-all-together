# lib/__init__.py
import sqlite3

# One shared connection & cursor for all modules
CONN = sqlite3.connect(':memory:')
CURSOR = CONN.cursor()
