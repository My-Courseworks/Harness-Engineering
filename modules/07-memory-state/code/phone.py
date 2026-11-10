"""The customer's phone, for the two-terminal demo: the one-time codes and other messages the bank sent them.

    python phone.py --user priya --var-dir var/adk/interactive            # what Priya's phone shows so far
    python phone.py --user priya --var-dir var/adk/interactive --follow   # keep watching (poll every 2 s)

It reads the bank's outbox (`outbound_messages`), which is the issuer's record of what it sent and where. The chat
command prints the same lines after each turn, so this is optional. Nothing here is visible to the agent.
"""

import argparse
import time
from pathlib import Path

from cardcare import world


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--user", required=True, choices=[c[0] for c in world.CUSTOMERS])
    parser.add_argument("--var-dir", type=Path, required=True, help="the chat's var dir, e.g. var/adk/interactive")
    parser.add_argument("--follow", action="store_true")
    args = parser.parse_args()
    bank = args.var_dir / "bank.db"
    shown = 0
    while True:
        if bank.exists():
            for m in world.outbound_messages(bank):
                if m["user_id"] == args.user and m["message_id"] > shown and m["status"] == "sent":
                    where = f"{m['channel']} to {m['destination']}" if m.get("destination") else m["channel"]
                    print(f"[{m['sent_at'] or m['drafted_at']}] [{where}] {m['body']}")
                    shown = m["message_id"]
        if not args.follow:
            break
        time.sleep(2)


if __name__ == "__main__":
    main()
