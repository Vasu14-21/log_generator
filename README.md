# Python SIEM-Style Log Generator

This project is a simple Python-based log generator designed to simulate realistic **SIEM-style logs** for training and practicing as a SOC (Security Operations Center) analyst.

It continuously generates logs with:

- Full timestamps
- Host and service (with PID)
- Structured tags like `[SECURITY][EVT1001][BRUTE_FORCE][HIGH]`
- Fields such as `user`, `role`, `from=<IP>`, `port`, `protocol`, `country`, `status`, `session_id`

The logs are printed in real time to the terminal and saved to rotating log files on disk.

---

## Features

- Continuous log generation (until you stop it)
- Real-time colored output in the terminal (with `colorama`, optional)
- Log file writing with basic rotation
- **SIEM-style structured events**, including:
  - Event types: `BRUTE_FORCE`, `LOGIN_SUCCESS`, `PRIV_ESC`, `ANOMALY`, `DOS`
  - Severities: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- Realistic fields:
  - Full timestamp `YYYY-MM-DD HH:MM:SS`
  - `host=<hostname>`
  - `<service>[<pid>]` (e.g. `sshd[4544]`, `nginx[1234]`)
  - Tags: `[LEVEL][EVTxxxx][EVENT_TYPE][SEVERITY]`
  - `user`, `role`
  - `from=<IP>`, `port=<port>`, `protocol=<protocol>`
  - `country=<ISO code>`
  - `status=<failed/success/suspicious>`
  - `session_id=<random>`

---

## Example Log Lines

Example security brute-force event:

```text
2026-02-22 16:13:36 host=db01 sshd[6738]: [WARNING][EVT2002][BRUTE_FORCE][HIGH] multiple failed password attempts user=charlie role=admin from=64.104.26.209 port=22 protocol=SSH country=US status=failed session_id=MBTRA9XD
```

Example successful login:

```text
2026-02-22 16:15:10 host=auth-gateway sshd[4544]: [INFO][EVT1002][LOGIN_SUCCESS][MEDIUM] Accepted password user=alice role=user from=155.212.55.29 port=22 protocol=SSH country=IN status=success session_id=483920
```

Example privilege escalation:

```text
2026-02-22 16:16:22 host=server sudo[9821]: [SECURITY][EVT3001][PRIV_ESC][CRITICAL] sudo command executed user=root role=admin from=10.0.0.5 port=22 protocol=SSH country=US status=success session_id=739201
```

Example anomaly / DOS:

```text
2026-02-22 16:17:05 host=web01 nginx[1204]: [ERROR][EVT5001][DOS][HIGH] high number of requests detected user=unknown role=user from=203.0.113.10 port=443 protocol=HTTP country=RU status=suspicious session_id=192837
2026-02-22 16:17:10 host=db01 kernel[8557]: [WARNING][EVT4001][ANOMALY][MEDIUM] unusual behavior detected user=alice role=devops from=58.15.107.128 port=3306 protocol=SYSTEM country=FR status=suspicious session_id=YFZENRO7
```

These lines are suitable for practicing:

- Detecting brute-force attacks
- Identifying successful logins after failures
- Spotting privilege escalation
- Investigating anomalies and possible DoS activity

---

## Project Structure

```text
loganalysis/
├── main.py        # Main Python script: log generator
└── logs/          # Log output directory (created automatically)
    └── auth.log  # Rotated log files
```

> Note: The `logs/` folder is created automatically when you run the script.

---

## Requirements

- **Python**: 3.8+
- **Optional**: `colorama` for colored terminal output

Install `colorama` (recommended):

```bash
pip install colorama
```

The script will still run without `colorama`, but output will be plain (no colors).

---

## Installation

1. Clone the project into a directory, for example:
   ```
2. Ensure `main.py` is present in this folder.

3. (Optional) Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install colorama
   ```

---

## Usage

### Basic Run (Continuous)

Start the log generator and let it run until you press `Ctrl + C`:

```bash
python main.py
```

- Logs print in real time to your terminal.
- Logs are saved to rotating files in the `logs/` directory.

### Limit Number of Logs (for testing)

Generate only a fixed number of logs (e.g. 50 lines):

```bash
python main.py --max-logs 50
```

### Change Delay Between Logs

Set delay between log entries (in seconds):

```bash
python main.py --delay 0.2
```

### Log File Rotation Settings

Set maximum log file size (in bytes) before rotation:

```bash
python main.py --max-size 50000
```

Change log directory and base log name:

```bash
python main.py --log-dir logs --log-name auth.log
```

This will create files like:

```text
logs/auth.log
```

---

## Command-line Arguments

`main.py` supports the following options:

- `--delay <float>`
  - Default: `0.5`
  - Description: Delay in seconds between log entries.

- `--max-logs <int>`
  - Default: `None` (infinite, until Ctrl+C)
  - Description: Maximum number of logs to generate before exiting (useful for testing).

- `--max-size <int>`
  - Default: `1048576` (1 MB)
  - Description: Maximum size (in bytes) of a log file before rotating to a new file.

- `--log-dir <path>`
  - Default: `logs`
  - Description: Directory where log files are stored.

- `--log-name <filename>`
  - Default: `auth.log`
  - Description: Base name for log files (timestamp is appended).

Example:

```bash
python main.py --delay 0.1 --max-logs 100 --max-size 200000 --log-dir logs --log-name auth.log
```

---

## Log Semantics (SOC / SIEM Perspective)

The generator produces events with internally consistent mappings:

- **Event Types → Messages**
  - `BRUTE_FORCE` → `multiple failed password attempts`
  - `LOGIN_SUCCESS` → `Accepted password`
  - `PRIV_ESC` → `sudo command executed`
  - `ANOMALY` → `unusual behavior detected`
  - `DOS` → `high number of requests detected`

- **Event Types → Severities**
  - `BRUTE_FORCE` → `HIGH`
  - `PRIV_ESC` → `CRITICAL`
  - `LOGIN_SUCCESS` → `MEDIUM`
  - `ANOMALY` → `LOW` or `MEDIUM` (random)
  - `DOS` → `HIGH`

- **Service ↔ Protocol Pairing**
  - `sshd` / `sudo` / `su` / `auth` → `SSH` protocol, typical ports `22`, `2022`, `2222`
  - `nginx`, `apache2` → `HTTP` protocol, typical ports `80`, `443`, `8080`
  - Other system services → `SYSTEM` protocol, ports like `3306`, `5432`, etc.

This means:

- You will not see mismatched combinations like `nginx` with `protocol=SSH`.
- `BRUTE_FORCE` always uses the correct message and severity.
- `LOGIN_SUCCESS` always uses `Accepted password`, `MEDIUM` severity, `status=success`.
- `PRIV_ESC` always uses `sudo command executed`, `CRITICAL` severity.

---

## Using This for SOC Training

Some ideas for practice:

- **Brute force detection**
  - Filter for `EVENT_TYPE=BRUTE_FORCE` or `message` containing `multiple failed password attempts`.
  - Correlate with `LOGIN_SUCCESS` from the same IP/user to simulate account compromise.

- **Privilege escalation**
  - Look for `EVENT_TYPE=PRIV_ESC`, `severity=CRITICAL`, and inspect affected users/hosts.

- **DoS / high traffic**
  - Focus on `EVENT_TYPE=DOS`, `protocol=HTTP`, and count hits per IP.

- **Anomalies**
  - Investigate `EVENT_TYPE=ANOMALY` to practice triaging suspicious but not clearly malicious behavior.

- **Session tracking**
  - Track `session_id` across multiple lines to simulate following a user/session through multiple stages.

You can also export generated logs to other tools (e.g., Splunk, ELK/Elastic, or open-source SIEMs) to practice searching and building detections.

---

## Stopping the Generator Safely

Press `Ctrl + C` in the terminal where the script is running.

The program:

- Catches `KeyboardInterrupt`
- Closes the current log file cleanly
- Prints a friendly shutdown message

---

🔍 Commands I Used for Log Separation:

To analyze and separate specific log types, I used various Linux commands:

1. Authentication / Security Logs (Failed password attempts, brute force detection)
grep "authentication failure" logs/auth.log
grep "Failed password" logs/auth.log
grep "Accepted password" logs/auth.log

2. System Logs (Kernel and system errors)
grep "kernel" logs/auth.log
grep "systemd" logs/auth.log

3. Application Logs (Application-level events, e.g., database failures, web server errors)
grep "ERROR" logs/auth.log
grep "application error" logs/auth.log

4. Web Server Logs (HTTP access, response status)
grep "GET" logs/auth.log
grep "POST" logs/auth.log

5. Firewall / Network Logs (Firewall events, network connection issues)
grep "firewalld" logs/auth.log
grep "network" logs/auth.log

6. IDS / IPS Logs (Intrusion attempts and alerts)
grep "IDS" logs/auth.log
grep "intrusion" logs/auth.log

7. Proxy Logs (Web proxy requests)
grep "proxy" logs/auth.log
grep "Web Proxy" logs/auth.log

8. DNS Logs (DNS queries, unusual traffic)
grep "DNS" logs/auth.log
grep "query" logs/auth.log

9. Email Logs (Email delivery, spam detection)
grep "email" logs/auth.log
grep "mail gateway" logs/auth.log

10. AV / EDR Logs (Malware detection and security events)
grep "AV" logs/auth.log
grep "EDR" logs/auth.log

11. Cloud / IAM / Audit Logs (User activity, cloud service logs)
grep "cloud" logs/auth.log
grep "audit" logs/auth.log

💡 Key Takeaways from the Project:
Simulating SOC Activities: The project allowed me to simulate a Security Operations Center (SOC) environment, where I monitored and analyzed various types of logs to detect suspicious activities.

Real-Time Log Monitoring: Used Linux commands like tail, grep, and awk to filter and separate specific log types for real-time analysis.

Log Filtering Skills: By using simple but effective Linux commands, I was able to focus on critical alerts, such as brute force attacks, failed login attempts, and privilege escalation.

## License

This project is for learning and SOC training purposes. Use and modify it freely for educational or lab environments.
