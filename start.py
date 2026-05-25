import os
import sys
import subprocess
import shutil

SUPPORTED_VERSIONS = [(3, 11), (3, 12)]

WINDOWS_PATHS = [
    r"%LOCALAPPDATA%\Programs\Python\Python311\python.exe",
    r"%LOCALAPPDATA%\Programs\Python\Python312\python.exe",
    r"C:\Python311\python.exe",
    r"C:\Python312\python.exe",
    r"C:\Program Files\Python311\python.exe",
    r"C:\Program Files\Python312\python.exe",
    r"C:\Program Files (x86)\Python311\python.exe",
    r"C:\Program Files (x86)\Python312\python.exe",
]

CANDIDATE_EXES = [
    ["py", "-3.11"],
    ["py", "-3.12"],
    ["python3.11"],
    ["python3.12"],
    ["python3.10"],
    ["python"],
]


def format_version(version):
    return f"{version[0]}.{version[1]}"


def is_supported(version):
    return tuple(version[:2]) in SUPPORTED_VERSIONS


def check_candidate(cmd):
    try:
        completed = subprocess.run(
            cmd + ["-c", "import sys; print(tuple(sys.version_info[:2]))"],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
        )
        if completed.returncode != 0:
            return None
        output = completed.stdout.strip()
        version = eval(output)
        if is_supported(version):
            return cmd
    except Exception:
        return None
    return None


def find_python():
    if is_supported(sys.version_info):
        return [sys.executable]

    if sys.platform == "win32":
        for path in WINDOWS_PATHS:
            path = os.path.expandvars(path)
            if os.path.exists(path):
                try:
                    completed = subprocess.run(
                        [path, "-c", "import sys; print(tuple(sys.version_info[:2]))"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        shell=False,
                    )
                    if completed.returncode == 0:
                        version = eval(completed.stdout.strip())
                        if is_supported(version):
                            return [path]
                except Exception:
                    pass

    for candidate in CANDIDATE_EXES:
        if candidate[0] != "python" and shutil.which(candidate[0]) is None:
            continue
        supported = check_candidate(candidate)
        if supported:
            return supported

    return None


def main():
    python_cmd = find_python()
    if python_cmd is None:
        print("ERROR: FaceVault requires Python 3.11 or 3.12.")
        print("Detected Python {}.{}.".format(*sys.version_info[:2]))
        print("Install Python 3.11 or 3.12 and ensure it is available on PATH.")
        print("On Windows, try installing from https://www.python.org/downloads/.")
        sys.exit(1)

    if python_cmd == [sys.executable] and is_supported(sys.version_info):
        os.execv(sys.executable, [sys.executable, "app.py"])
    else:
        version_output = subprocess.run(
            python_cmd + ["-c", "import sys; print(tuple(sys.version_info[:2]))"],
            capture_output=True,
            text=True,
        ).stdout.strip()
        version = eval(version_output)
        print(f"Launching FaceVault with Python {format_version(version)}...")
        os.execv(python_cmd[0], python_cmd + ["app.py"])


if __name__ == "__main__":
    main()
