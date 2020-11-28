import argparse
import os
import sys

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, "Requires Python 3.7 or newer"

os.sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    parser = argparse.ArgumentParser(description='')
    cmd_list = (
        "sync",
        "create_db",
        "drop_db"
    )

    parser.add_argument("cmd", choices=cmd_list, nargs="?", default="")

    args = parser.parse_args()
    cmd = args.cmd

    if cmd == "sync":
        from stacks_monitor.sync import main
        main()

    if cmd == "create_db":
        from stacks_monitor.db_tool import create_db
        create_db()

    if cmd == "drop_db":
        from stacks_monitor.db_tool import drop_db
        drop_db()


if __name__ == '__main__':
    main()
