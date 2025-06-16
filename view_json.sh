#!/bin/bash
# Script to safely view large JSON files

echo "📊 Step1.json File Info:"
echo "Size: $(ls -lh step1.json | awk '{print $5}')"
echo "Lines: $(wc -l < step1.json)"
echo ""

echo "🔍 Quick Preview Options:"
echo "1. First 50 lines:"
echo "   head -50 step1.json"
echo ""
echo "2. Last 50 lines:" 
echo "   tail -50 step1.json"
echo ""
echo "3. Structure overview:"
echo "   jq 'keys' step1.json"
echo ""
echo "4. Live matches count:"
echo "   jq '.live_matches.results | length' step1.json"
echo ""
echo "5. Create small sample (first 100 lines):"
echo "   head -100 step1.json > step1_sample.json"
echo ""

# Auto-create sample
echo "📝 Creating step1_sample.json (first 200 lines)..."
head -200 step1.json > step1_sample.json
echo "✅ Created step1_sample.json ($(ls -lh step1_sample.json | awk '{print $5}'))"