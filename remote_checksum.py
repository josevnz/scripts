#!/usr/bin/env python3
import argparse
import traceback
import sys
import random
import time
from _socket import gaierror
from pathlib import Path
import paramiko
from paramiko import SSHException, SSHClient, AutoAddPolicy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate the checksum of remote files to make sure they are not tampered')
    parser.add_argument('--retries', action='store', default=10, help='SSH retry override')
    parser.add_argument('--server', action='store', required=True, help='Name of the remote server with the files')
    parser.add_argument('--remotepath', action='store', required=True, help='Remote path with files that need will get their sha256 calculated')
    parser.add_argument('report', action='store', help='Report destination')
    args = parser.parse_args()
    with SSHClient() as client:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        key = paramiko.rsakey.RSAKey.from_private_key_file(str(Path.home().joinpath('.ssh').joinpath('id_rsa')))
        attempt = 1
        while attempt < args.retries:
            try:
                client.connect(hostname=args.server, pkey=key, banner_timeout=300, timeout=300)
                REMOTE_CMD = f'/usr/bin/find {args.remotepath} -type f| /usr/bin/xargs /usr/bin/sha256sum --binary'
                print(f"SSH connected to {args.server}, getting remote checksums. It will take a while...")
                stdin, stdout, stderr = client.exec_command(REMOTE_CMD)
                with open(args.report, 'w') as rfh:
                    for line in stdout.readlines():
                        rfh.write(line)
                        print(line.strip(), file=sys.stdout)
                for line in stderr.readlines():
                    print(line.strip(), file=sys.stderr)
                break
            except (SSHException, gaierror):
                wait_time = int(random.uniform(1, 60))
                print(f"ERROR: Could not connect, will try again in {wait_time} seconds ({attempt})", file=sys.stdout)
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
                time.sleep(wait_time)
                attempt += 1
