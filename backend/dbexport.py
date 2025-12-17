import psycopg2
from psycopg2.extras import DictCursor

# Local database connection
local_conn = psycopg2.connect("postgresql://postgres:anvi02@localhost:5432/treegrid")
local_cur = local_conn.cursor(cursor_factory=DictCursor)

# Neon connection
neon_conn = psycopg2.connect("postgresql://neondb_owner:npg_uUmt2pPj6Oke@ep-late-wave-a4ykohb8-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")
neon_cur = neon_conn.cursor()

# Get all tables
local_cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
""")
tables = [row[0] for row in local_cur.fetchall()]

for table in tables:
    # Get data
    local_cur.execute(f"SELECT * FROM {table}")
    rows = local_cur.fetchall()
    
    if not rows:
        continue
        
    # Get column names
    col_names = [desc[0] for desc in local_cur.description]
    cols = ', '.join(col_names)
    placeholders = ', '.join(['%s'] * len(col_names))
    
    # Insert into Neon
    insert_sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    neon_cur.executemany(insert_sql, rows)
    neon_conn.commit()

local_cur.close()
local_conn.close()
neon_cur.close()
neon_conn.close()