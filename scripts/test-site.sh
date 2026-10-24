#!/bin/bash
# Site Build and Test Script
# Runs the site build and all validation checks

set -e  # Exit on error

echo "=========================================="
echo "Site Build and Test Automation"
echo "=========================================="
echo ""

# Check if site/build.py exists
if [ ! -f "site/build.py" ]; then
    echo "ERROR: site/build.py not found"
    exit 1
fi

# Run the site build
echo "Building site..."
python site/build.py

if [ $? -ne 0 ]; then
    echo "ERROR: Site build failed"
    exit 1
fi

echo ""
echo "✓ Site build successful"
echo ""

# Run check_site.py
echo "Running site validation checks..."
python site/check_site.py --live

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Site validation failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ All tests passed!"
echo "=========================================="
