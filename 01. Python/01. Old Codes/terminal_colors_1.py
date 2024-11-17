class TerminalColors:
    # Basic Colors
    RED = "\033[91m"       # Red, typically used for errors or critical issues
    GREEN = "\033[92m"     # Green, typically used for success or completion
    YELLOW = "\033[93m"    # Yellow, typically used for warnings or cautions
    BLUE = "\033[94m"      # Blue, typically used for informational messages
    MAGENTA = "\033[95m"   # Magenta, for special or highlighted messages
    CYAN = "\033[96m"      # Cyan, for informational or important messages
    WHITE = "\033[97m"     # White, for neutral or standard messages
    RESET = "\033[0m"      # Reset color to default

    # Extended Colors (For more specific use cases)
    ORANGE = "\033[38;5;214m"  # Orange, can be used for warnings or alerts
    PURPLE = "\033[38;5;128m"  # Purple, for things that need attention or secondary info
    BOLD_RED = "\033[1;91m"    # Bold red for critical errors or urgent messages
    BOLD_GREEN = "\033[1;92m"  # Bold green for key success or important completions
    UNDERLINE_YELLOW = "\033[4;93m"  # Underlined yellow for caution or attention
    UNDERLINE_BLUE = "\033[4;94m"    # Underlined blue for informative, but urgent messages
    BRIGHT_WHITE = "\033[1;97m"      # Bright white for neutral info, but emphasized

    # Background Colors
    BG_RED = "\033[41m"     # Red background, usually for errors
    BG_GREEN = "\033[42m"   # Green background, success messages
    BG_YELLOW = "\033[43m"  # Yellow background, warnings
    BG_BLUE = "\033[44m"    # Blue background, general info
    BG_MAGENTA = "\033[45m" # Magenta background, special notes
    BG_CYAN = "\033[46m"    # Cyan background, important notes
    BG_WHITE = "\033[47m"   # White background, neutral messages
    BG_RESET = "\033[49m"   # Reset background color
