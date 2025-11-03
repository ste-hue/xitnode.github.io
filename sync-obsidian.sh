#!/bin/bash

# Obsidian to Jekyll Sync Script
# Simple wrapper for convert_obsidian.py

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/convert_obsidian.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_help() {
    echo -e "${BLUE}🚀 Obsidian to Jekyll Sync${NC}"
    echo -e "${BLUE}=========================${NC}"
    echo ""
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  retro, r, back       Convert with retroactive dates (today → backwards)"
    echo "  prog, p, forward     Convert with progressive dates (today → forwards)"
    echo "  dry, test            Show what would be converted (dry run)"
    echo "  help, h              Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 retro             # Convert with dates going backwards from today"
    echo "  $0 prog              # Convert with dates going forwards from today"
    echo "  $0 dry               # Preview what would be converted"
    echo ""
}

check_python_script() {
    if [[ ! -f "$PYTHON_SCRIPT" ]]; then
        echo -e "${RED}❌ Python script not found: $PYTHON_SCRIPT${NC}"
        exit 1
    fi
}

run_conversion() {
    local mode=$1
    local extra_args=$2

    echo -e "${GREEN}🔄 Running conversion in $mode mode...${NC}"
    echo ""

    python3 "$PYTHON_SCRIPT" --mode "$mode" $extra_args ${OBSIDIAN_ROOT:+--obsidian-path "$OBSIDIAN_ROOT"}
}

main() {
    check_python_script

    case "${1:-}" in
        "retro"|"r"|"back"|"")
            run_conversion "retroactive"
            ;;
        "prog"|"p"|"forward")
            run_conversion "progressive"
            ;;
        "dry"|"test")
            echo -e "${YELLOW}🔍 Running dry run (retroactive mode)...${NC}"
            echo ""
            python3 "$PYTHON_SCRIPT" --mode "retroactive" --dry-run ${OBSIDIAN_ROOT:+--obsidian-path "$OBSIDIAN_ROOT"}
            ;;
        "help"|"h"|"-h"|"--help")
            print_help
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo ""
            print_help
            exit 1
            ;;
    esac
}

main "$@"
