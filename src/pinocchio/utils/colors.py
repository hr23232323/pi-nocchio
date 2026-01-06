"""Simple ANSI color codes for terminal output (no dependencies)."""


class Colors:
    """ANSI escape codes for terminal colors."""

    # Colors
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    RED = "\033[91m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @staticmethod
    def cyan(text: str) -> str:
        """Return text in cyan."""
        return f"{Colors.CYAN}{text}{Colors.RESET}"

    @staticmethod
    def green(text: str) -> str:
        """Return text in green."""
        return f"{Colors.GREEN}{text}{Colors.RESET}"

    @staticmethod
    def yellow(text: str) -> str:
        """Return text in yellow."""
        return f"{Colors.YELLOW}{text}{Colors.RESET}"

    @staticmethod
    def magenta(text: str) -> str:
        """Return text in magenta."""
        return f"{Colors.MAGENTA}{text}{Colors.RESET}"

    @staticmethod
    def blue(text: str) -> str:
        """Return text in blue."""
        return f"{Colors.BLUE}{text}{Colors.RESET}"

    @staticmethod
    def bold(text: str) -> str:
        """Return text in bold."""
        return f"{Colors.BOLD}{text}{Colors.RESET}"

    @staticmethod
    def dim(text: str) -> str:
        """Return text dimmed."""
        return f"{Colors.DIM}{text}{Colors.RESET}"


def print_banner(agent_name: str, version: str = "0.1.0") -> None:
    """Print a welcome banner."""
    print()
    print(Colors.magenta("╔════════════════════════════════════════════════════════════╗"))
    print(
        Colors.magenta("║") + f"  {Colors.bold(agent_name)} v{version} - Ready to become real! ✨      " + Colors.magenta("║")
    )
    print(Colors.magenta("╚════════════════════════════════════════════════════════════╝"))
    print()
