import argparse
import os
import random
import time
from datetime import datetime

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
except ImportError:
    class _DummyColor:
        def __getattr__(self, name):
            return ""

    Fore = _DummyColor()
    Style = _DummyColor()


LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_SECURITY = "SECURITY"


LEVEL_COLORS = {
    LOG_LEVEL_INFO: Fore.GREEN,
    LOG_LEVEL_WARNING: Fore.YELLOW,
    LOG_LEVEL_ERROR: Fore.RED,
    LOG_LEVEL_SECURITY: Fore.MAGENTA,
}


HOSTNAMES = ["server", "web01", "db01", "auth-gateway"]
USERNAMES = [
    "root",
    "admin",
    "alice",
    "bob",
    "charlie",
    "deploy",
    "monitor",
    "backup",
]

SECURITY_SOURCES = ["sshd", "sudo", "su", "auth"]
INFO_SOURCES = ["systemd", "cron", "kernel", "nginx", "apache2"]
WARNING_SOURCES = ["kernel", "nginx", "apache2", "firewalld"]
ERROR_SOURCES = ["systemd", "app", "postgres", "nginx", "apache2"]
ROLES = ["admin", "user", "devops", "security", "dbadmin"]
COUNTRIES = ["US", "UK", "DE", "FR", "IN", "CN", "RU", "BR", "AU", "ZA"]


def format_timestamp() -> str:
    """
    Return a full timestamp string like '2026-02-22 11:26:15'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def random_ip() -> str:
    """
    Generate a random IPv4 address string.
    """
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def random_hostname() -> str:
    """
    Pick a random hostname for the log entry.
    """
    return random.choice(HOSTNAMES)


def random_pid() -> int:
    """
    Generate a random process ID.
    """
    return random.randint(100, 9999)


def random_session_id(length: int = 8) -> str:
    """
    Generate a random session identifier.
    """
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))


def generate_info_log() -> tuple[str, str]:
    """
    Generate a single INFO-type log entry.
    Returns a tuple of (log_level, formatted_log_line).
    """
    timestamp = format_timestamp()
    hostname = random_hostname()
    source = random.choice(INFO_SOURCES)
    pid = random_pid()
    user = random.choice(USERNAMES)
    role = random.choice(ROLES)
    ip = random_ip()
    session_id = random_session_id()

    messages = [
        "normal activity",
        "user login success",
        "configuration reload completed",
        "health check passed",
    ]

    event_id = "EVT0001"
    category = "NORMAL_ACTIVITY"
    severity = "LOW"
    status = "success"
    message = random.choice(messages)

    log_line = (
        f"{timestamp} host={hostname} {source}[{pid}]: "
        f"[{LOG_LEVEL_INFO}][{event_id}][{category}][{severity}] "
        f"{message} user={user} role={role} from={ip} status={status} session_id={session_id}"
    )
    return LOG_LEVEL_INFO, log_line


def generate_warning_log() -> tuple[str, str]:
    """
    Generate a single WARNING-type log entry.
    Returns a tuple of (log_level, formatted_log_line).
    """
    timestamp = format_timestamp()
    hostname = random_hostname()
    source = random.choice(WARNING_SOURCES)
    pid = random_pid()
    user = random.choice(USERNAMES)
    role = random.choice(ROLES)
    ip = random_ip()
    country = random.choice(COUNTRIES)
    session_id = random_session_id()

    messages = [
        "possible brute force behaviour detected",
        "unusual number of requests",
        "high memory usage detected",
        "multiple failed password attempts",
    ]

    event_id = "EVT2001"
    category = "ANOMALY"
    severity = "MEDIUM"
    status = "suspicious"
    message = random.choice(messages)

    log_line = (
        f"{timestamp} host={hostname} {source}[{pid}]: "
        f"[{LOG_LEVEL_WARNING}][{event_id}][{category}][{severity}] "
        f"{message} user={user} role={role} from={ip} country={country} status={status} session_id={session_id}"
    )
    return LOG_LEVEL_WARNING, log_line


def generate_error_log() -> tuple[str, str]:
    """
    Generate a single ERROR-type log entry.
    Returns a tuple of (log_level, formatted_log_line).
    """
    timestamp = format_timestamp()
    hostname = random_hostname()
    source = random.choice(ERROR_SOURCES)
    pid = random_pid()
    ip = random_ip()
    session_id = random_session_id()

    messages = [
        f"service crashed with exit code {random.randint(1, 255)}",
        "database connection failed",
        "application error: unhandled exception",
        "failed to start worker process",
        "disk I/O error on /var/log",
    ]

    event_id = "EVT3001"
    category = "SYSTEM_ERROR"
    severity = "HIGH"
    status = "failed"
    message = random.choice(messages)

    log_line = (
        f"{timestamp} host={hostname} {source}[{pid}]: "
        f"[{LOG_LEVEL_ERROR}][{event_id}][{category}][{severity}] "
        f"{message} from={ip} status={status} session_id={session_id}"
    )
    return LOG_LEVEL_ERROR, log_line


def generate_security_log() -> tuple[str, str]:
    """
    Generate a single SECURITY-type log entry simulating auth.log style events.
    Returns a tuple of (log_level, formatted_log_line).
    """
    timestamp = format_timestamp()
    hostname = random_hostname()
    source = random.choice(SECURITY_SOURCES)
    pid = random_pid()
    ip = random_ip()
    user = random.choice(USERNAMES + ["invalid", "unknown", "test"])
    role = random.choice(ROLES)
    port = random.choice([22, 2022, 2222])
    country = random.choice(COUNTRIES)
    session_id = random_session_id()

    patterns = [
        {
            "event_id": "EVT1001",
            "attack_type": "BRUTE_FORCE",
            "severity": "HIGH",
            "message": "authentication failure",
            "status": "failed",
        },
        {
            "event_id": "EVT1002",
            "attack_type": "FAILED_LOGIN",
            "severity": "MEDIUM",
            "message": "failed password",
            "status": "failed",
        },
        {
            "event_id": "EVT1003",
            "attack_type": "SUCCESSFUL_LOGIN",
            "severity": "LOW",
            "message": "accepted password",
            "status": "success",
        },
    ]

    pattern = random.choice(patterns)

    log_line = (
        f"{timestamp} host={hostname} {source}[{pid}]: "
        f"[{LOG_LEVEL_SECURITY}][{pattern['event_id']}][{pattern['attack_type']}][{pattern['severity']}] "
        f"{pattern['message']} user={user} role={role} from={ip} port={port} country={country} "
        f"status={pattern['status']} session_id={session_id}"
    )
    return LOG_LEVEL_SECURITY, log_line


def generate_random_log_entry() -> tuple[str, str]:
    """
    Randomly choose a log type and generate an appropriate log entry.
    Returns a tuple of (log_level, formatted_log_line).
    """
    choice = random.random()
    if choice < 0.5:
        return generate_info_log()
    if choice < 0.7:
        return generate_warning_log()
    if choice < 0.85:
        return generate_error_log()
    return generate_security_log()


class LogRotator:
    """
    Simple log file rotator that creates a new log file when size exceeds a limit.
    """

    def __init__(self, log_dir: str, base_filename: str, max_bytes: int) -> None:
        self.log_dir = log_dir
        self.base_filename = base_filename
        self.max_bytes = max_bytes
        os.makedirs(self.log_dir, exist_ok=True)
        self.current_file = self._open_new_file()

    def _open_new_file(self):
        """
        Open a new log file with a timestamp-based name.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(self.base_filename)
        filename = f"{name}_{timestamp}{ext or '.log'}"
        full_path = os.path.join(self.log_dir, filename)
        return open("auth.log", "a", encoding="utf-8")

    def _needs_rotation(self) -> bool:
        """
        Check whether the current log file should be rotated based on its size.
        """
        try:
            return self.current_file.tell() >= self.max_bytes
        except ValueError:
            return False

    def write_line(self, line: str) -> None:
        """
        Write a single log line to the current file, rotating if needed.
        """
        if self._needs_rotation():
            self.current_file.close()
            self.current_file = self._open_new_file()
        self.current_file.write(line + "\n")
        self.current_file.flush()

    def close(self) -> None:
        """
        Close the current log file safely.
        """
        try:
            if not self.current_file.closed:
                self.current_file.close()
        except Exception:
            pass


def parse_args():
    """
    Parse command-line arguments for the log generator.
    """
    parser = argparse.ArgumentParser(description="Simple Python-based log generator.")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay in seconds between log entries.",
    )
    parser.add_argument(
        "--max-logs",
        type=int,
        default=None,
        help="Maximum number of log entries to generate before exiting "
        "(useful for testing). If not set, runs until interrupted.",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024 * 1024,
        help="Maximum size in bytes for a log file before rotation.",
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="logs",
        help="Directory where log files will be stored.",
    )
    parser.add_argument(
        "--log-name",
        type=str,
        default="auth.log",
        help="Base filename for log files.",
    )
    return parser.parse_args()


def run_log_generator() -> None:
    """
    Main loop that continuously generates logs, prints them, and writes to files.
    Handles Ctrl+C for safe shutdown.
    """
    args = parse_args()
    rotator = LogRotator(
        log_dir=args.log_dir,
        base_filename=args.log_name,
        max_bytes=args.max_size,
    )

    print("Starting log generator. Press Ctrl+C to stop.", flush=True)

    count = 0
    try:
        while True:
            level, line = generate_random_log_entry()

            color = LEVEL_COLORS.get(level, "")
            reset = getattr(Style, "RESET_ALL", "")
            print(f"{color}{line}{reset}", flush=True)

            rotator.write_line(line)

            count += 1
            if args.max_logs is not None and count >= args.max_logs:
                break

            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\nCtrl+C received, stopping log generator...", flush=True)
    finally:
        rotator.close()
        print("Log generator stopped. Log file closed.", flush=True)


if __name__ == "__main__":
    run_log_generator()

def generate_random_log_entry() -> tuple[str, str]:
    """
    Generate a single SIEM-style log entry with consistent EVENT_TYPE, SEVERITY,
    message, protocol and fields.

    Returns a tuple of (log_level, formatted_log_line).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = random_hostname()
    pid = random_pid()
    user = random.choice(USERNAMES + ["invalid", "unknown", "test"])
    role = random.choice(["user", "admin"])
    ip = random_ip()
    country = random.choice(["IN", "US", "RU", "DE", "FR", "UK", "CN", "BR", "AU"])
    session_id = str(random.randint(100000, 999999))

    # Event definitions: mapping EVENT_TYPE → message, severity, status, level, event_id
    event_definitions = {
        "BRUTE_FORCE": {
            "message": "multiple failed password attempts",
            "severity": "HIGH",
            "status": "failed",
            "level": LOG_LEVEL_WARNING,
            "event_id": "EVT2002",
        },
        "LOGIN_SUCCESS": {
            "message": "Accepted password",
            "severity": "MEDIUM",
            "status": "success",
            "level": LOG_LEVEL_INFO,
            "event_id": "EVT1002",
        },
        "PRIV_ESC": {
            "message": "sudo command executed",
            "severity": "CRITICAL",
            "status": "success",
            "level": LOG_LEVEL_SECURITY,
            "event_id": "EVT3001",
        },
        "ANOMALY": {
            "message": "unusual behavior detected",
            "severity": random.choice(["LOW", "MEDIUM"]),
            "status": "suspicious",
            "level": LOG_LEVEL_WARNING,
            "event_id": "EVT4001",
        },
        "DOS": {
            "message": "high number of requests detected",
            "severity": "HIGH",
            "status": "suspicious",
            "level": LOG_LEVEL_ERROR,
            "event_id": "EVT5001",
        },
    }

    # Choose an event type
    event_type = random.choice(list(event_definitions.keys()))
    event_cfg = event_definitions[event_type]

    # Map service ↔ protocol realistically based on event type
    if event_type in ("BRUTE_FORCE", "LOGIN_SUCCESS"):
        source = "sshd"
        protocol = "SSH"
        port = random.choice([22, 2022, 2222])
    elif event_type == "PRIV_ESC":
        source = "sudo"
        protocol = "SSH"
        port = random.choice([22, 2022])
    elif event_type == "DOS":
        source = random.choice(["nginx", "apache2"])
        protocol = "HTTP"
        port = random.choice([80, 443, 8080])
    else:  # ANOMALY or any future generic anomaly-type
        # Pick from a mix of system and app services
        possibles = INFO_SOURCES + WARNING_SOURCES + ERROR_SOURCES
        source = random.choice(possibles)
        service_protocol_map = {
            "nginx": "HTTP",
            "apache2": "HTTP",
            "sshd": "SSH",
            "sudo": "SSH",
            "su": "SSH",
            "auth": "SSH",
        }
        protocol = service_protocol_map.get(source, "SYSTEM")
        if protocol == "HTTP":
            port = random.choice([80, 443, 8080])
        elif protocol == "SSH":
            port = random.choice([22, 2022, 2222])
        else:
            port = random.choice([22, 80, 443, 3306, 5432])

    level = event_cfg["level"]
    event_id = event_cfg["event_id"]
    severity = event_cfg["severity"]
    message = event_cfg["message"]
    status = event_cfg["status"]

    log_line = (
        f"{timestamp} host={hostname} {source}[{pid}]: "
        f"[{level}][{event_id}][{event_type}][{severity}] "
        f"{message} user={user} role={role} from={ip} port={port} "
        f"protocol={protocol} country={country} status={status} "
        f"session_id={session_id}"
    )

    return level, log_line