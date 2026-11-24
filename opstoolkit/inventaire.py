#!/usr/bin/env python3

serveurs = [
    {"name": "web01", "role": "web",   "up": True,  "cpu": 45},
    {"name": "db01", "role": "db",    "up": True, "cpu": 92},
    {"name": "web02", "role": "web",   "up": False, "cpu": 85},
    {"name": "cache01", "role": "cache", "up": True,  "cpu": 30},
]


def count_by_role(servers):
    counts = {}
    for s in servers:
        counts[s["role"]] = counts.get(s["role"], 0) + 1
    return counts

def down_servers(servers):
    counts = []
    for s in servers:
        if s["up"] is False:
            counts.append(s["name"])
    return counts

def overloaded(servers, threshold=90):
    noms = []
    for s in servers:
        if s["cpu"] > threshold:
            noms.append(s["name"])
    return noms

##def decrescent(servers):
        

def main():
        print(count_by_role(serveurs))

if __name__ == "__main__":
    main()

