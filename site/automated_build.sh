#!/bin/bash
# Automated build and test script for the drift repository
# Runs build.py and check_site.py to ensure the site is properly built and valid

set -e  # Exit on any error

echo "=================================="
echo "Drift Site Automated Build"
echo "=================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall success
BUILD_SUCCESS=0
CHECK_SUCCESS=0

# Step 1: Build the site
echo -e "${YELLOW}Step 1: Building site...${NC}"
if python site/build.py; then
    echo -e "${GREEN}✓ Site build successful${NC}"
    BUILD_SUCCESS=1
else
    echo -e "${RED}✗ Site build failed${NC}"
    BUILD_SUCCESS=0
fi
echo ""

# Step 2: Check site validity
echo -e "${YELLOW}Step 2: Checking site validity...${NC}"
if python site/check_site.py --live; then
    echo -e "${GREEN}✓ Site validation passed${NC}"
    CHECK_SUCCESS=1
else
    echo -e "${RED}✗ Site validation failed${NC}"
    CHECK_SUCCESS=0
fi
echo ""

# Final result
echo "=================================="
if [ $BUILD_SUCCESS -eq 1 ] && [ $CHECK_SUCCESS -eq 1 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    if [ $BUILD_SUCCESS -eq 0 ]; then
        echo "  - Site build failed"
    fi
    if [ $CHECK_SUCCESS -eq 0 ]; then
        echo "  - Site validation failed"
    fi
    exit 1
fi
