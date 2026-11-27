import argparse
import json
import logging
import socket
import sys
import time

import requests
import yaml

log = logging.getLogger("watchdog")


def load_targets(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as e:
        raise ValueError(f"Fichier de cibles invalide : {e}")
    if not isinstance(data, dict) or not isinstance(data.get("targets"), list):
        raise ValueError("Fichier de cibles invalide : clé 'targets' absente")
    for t in data["targets"]:
        if not isinstance(t, dict):
            raise ValueError("Fichier de cibles invalide : cible mal formée")
        for key in ("name", "host", "port"):
            if key not in t:
                raise ValueError(f"Fichier de cibles invalide : '{key}' manquant")
    return data["targets"]


def check_port(host, port, timeout=2.0):
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
    except OSError:
        return False, None
    return True, int((time.perf_counter() - start) * 1000)


def check_http(url, timeout=2.0):
    try:
        return requests.get(url, timeout=timeout).status_code == 200
    except requests.RequestException:
        return False


def check_target(target):
    ok, ms = check_port(target["host"], target["port"])
    if ok and target.get("health_url"):
        ok = check_http(target["health_url"])
    return {"name": target["name"], "ok": ok, "ms": ms}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("targets_file")
    parser.add_argument("-o", "--output", default="watchdog-report.json")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        format="%(levelname)s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    try:
        targets = load_targets(args.targets_file)
    except ValueError as e:
        log.error("%s", e)
        return 2

    report = []
    for t in targets:
        result = check_target(t)
        log.info("%s : %s", result["name"], "OK" if result["ok"] else "KO")
        report.append(result)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return 0 if all(r["ok"] for r in report) else 1


if __name__ == "__main__":
    sys.exit(main())
