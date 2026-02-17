#!/bin/bash

# FIX 1: SQL 'values' reserved word error
# FIX 2: save_upload() argument mismatch

echo "🔧 Applying critical fixes..."
echo ""

cd /home/localadmin/ultimate_ai_v8

# Fix 1: Rename 'values' table to 'ai_values' in schema.py
echo "Fix 1: Renaming 'values' table to 'ai_values'..."
sed -i "s/CREATE TABLE IF NOT EXISTS values (/CREATE TABLE IF NOT EXISTS ai_values (/" src/database/schema.py
sed -i "s/FROM values/FROM ai_values/g" src/database/schema.py
sed -i "s/INTO values/INTO ai_values/g" src/database/schema.py
echo "✅ Table renamed"

# Fix 2: Update main.py to pass filename to save_upload
echo "Fix 2: Fixing save_upload() call in main.py..."
sed -i "s/success, context_or_error = file_service.save_upload(file)/success, context_or_error = file_service.save_upload(file, file.filename)/" main.py
echo "✅ Upload fixed"

# Fix 3: Rename 'values' table in schema_FIXED.py too
if [ -f "src/database/schema_FIXED.py" ]; then
    sed -i "s/CREATE TABLE IF NOT EXISTS values (/CREATE TABLE IF NOT EXISTS ai_values (/" src/database/schema_FIXED.py
    echo "✅ schema_FIXED.py updated too"
fi

echo ""
echo "🔄 Reinitializing database..."
python3 src/database/schema.py

echo ""
echo "🚀 Restarting AI..."
./stop.sh 2>/dev/null || true
sleep 1
./start.sh

echo ""
echo "✅ All fixes applied!"
