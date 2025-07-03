import re
from datetime import datetime

def parse_log(log_line):
    """
    Enhanced log parser that handles multiple log formats
    """
    line = log_line.strip()
    if not line:
        raise ValueError("Empty log line")

    # Common log format patterns
    patterns = [
        # Simple format: date ip status
        r'^(\S+)\s+(\S+)\s+(\d+).*$',
        # Apache Common Log Format
        r'^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\].*?"\s*(\d+)\s.*$',
        # Extended format with timestamp
        r'^(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\d+).*$'
    ]

    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            date, ip, status = match.groups()

            # Validate IP address format
            if not is_valid_ip(ip):
                raise ValueError(f"Invalid IP address format: {ip}")

            # Validate status code
            if not status.isdigit() or not (100 <= int(status) <= 599):
                raise ValueError(f"Invalid HTTP status code: {status}")

            return {
                "date": date,
                "ip": ip,
                "status": int(status),
                "status_category": get_status_category(int(status))
            }

    raise ValueError(f"Unrecognized log format: {line[:50]}...")

def is_valid_ip(ip):
    """Basic IP address validation"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

def get_status_category(status):
    """Categorize HTTP status codes"""
    if 100 <= status < 200:
        return "Informational"
    elif 200 <= status < 300:
        return "Success"
    elif 300 <= status < 400:
        return "Redirection"
    elif 400 <= status < 500:
        return "Client Error"
    elif 500 <= status < 600:
        return "Server Error"
    else:
        return "Unknown"