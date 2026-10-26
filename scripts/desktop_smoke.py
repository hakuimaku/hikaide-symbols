#!/usr/bin/env python3
"""Smoke-test installed file managers on private Broadway/DBus test sessions."""
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from theme import ROOT, THEME, VARIANTS


def smoke(binary, gtk, mode="dark"):
    """Start one application with a private icon-theme selection."""
    theme_name = VARIANTS[mode]
    theme = THEME.parent / theme_name
    server = "broadwayd" if gtk == 3 else "gtk4-broadwayd"
    if not shutil.which(binary) or not shutil.which(server):
        return {"application": binary, "status": "not installed"}
    with tempfile.TemporaryDirectory(prefix="hikaide-desktop-test-") as tmp:
        base = Path(tmp)
        for name in ("config", "data", "cache", "state", "run"):
            (base / name).mkdir(mode=0o700)
        icons = base / "data/icons"
        icons.mkdir()
        (icons / theme_name).symlink_to(theme, target_is_directory=True)
        for version in (3, 4):
            folder = base / f"config/gtk-{version}.0"
            folder.mkdir()
            (folder / "settings.ini").write_text(f"[Settings]\ngtk-icon-theme-name={theme_name}\n")
        env = {**os.environ, "XDG_CONFIG_HOME": str(base / "config"), "XDG_DATA_HOME": str(base / "data"),
               "XDG_CACHE_HOME": str(base / "cache"), "XDG_STATE_HOME": str(base / "state"), "XDG_RUNTIME_DIR": str(base / "run"),
               "GDK_BACKEND": "broadway", "BROADWAY_DISPLAY": ":9", "GSK_RENDERER": "cairo", "GSETTINGS_BACKEND": "keyfile",
               "GIO_USE_VFS": "local", "GVFS_DISABLE_FUSE": "1"}
        processes = []
        with (base / "server.log").open("w+") as log:
            try:
                daemon = subprocess.Popen([server, "--unixsocket", str(base / "http.socket"), ":9"], env=env,
                                          stdout=log, stderr=log, start_new_session=True)
                processes.append(daemon)
                for _ in range(50):
                    if list((base / "run").glob("broadway*.socket")) or daemon.poll() is not None:
                        break
                    time.sleep(.02)
                if daemon.poll() is not None:
                    log.seek(0)
                    raise RuntimeError(log.read())
                query = "gtk-query-settings" if gtk == 3 else "gtk4-query-settings"
                settings = subprocess.run([query], env=env, capture_output=True, text=True, timeout=5)
                selected = next((s.strip() for s in settings.stdout.splitlines() if "gtk-icon-theme-name:" in s), "")
                assert selected == f'gtk-icon-theme-name: "{theme_name}"', (binary, selected, settings.stderr)
                command = ["dbus-run-session", "--", binary]
                command += ["--new-window", str(ROOT / "docs")] if binary == "nautilus" else [str(ROOT / "docs")]
                with (base / "app.log").open("w+") as app_log:
                    app = subprocess.Popen(command, env=env, stdout=app_log, stderr=app_log, start_new_session=True)
                    processes.append(app)
                    try:
                        code = app.wait(timeout=4)
                    except subprocess.TimeoutExpired:
                        code = None
                    app_log.seek(0)
                    messages = app_log.read()
                    assert code is None, f"{binary} exited during smoke check: {code}\n{messages}"
                    return {"application": binary, "gtk": gtk, "status": "pass: alive after 4 seconds",
                            "backend": "private Broadway", "theme_setting": selected,
                            "scope": "startup smoke; no interactive browsing or visual window review",
                            "diagnostics": messages[-3500:]}
            finally:
                for process in reversed(processes):
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()


if __name__ == "__main__":
    results = [{"variant": mode, **smoke(binary, gtk, mode)}
               for mode in VARIANTS for binary, gtk in (("nautilus", 4), ("thunar", 3))]
    target = ROOT / "reports/desktop-smoke.json"
    target.write_text(json.dumps(results, indent=2) + "\n")
    print(target.read_text())
