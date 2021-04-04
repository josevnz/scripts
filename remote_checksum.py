#!/usr/bin/env python3
import argparse
import traceback
import sys
import os
import random
import time
import paramiko
from paramiko import SSHException, SSHClient, AutoAddPolicy

CHECKSUM_RSA_KEY_FILE = os.environ['CHECKSUM_RSA_KEY_FILE']
CHECKSUM_REMOTE_SERVER = os.environ['CHECKSUM_REMOTE_SERVER']
REMOTE_CMD='/usr/bin/find {CHECKSUM_PATH} -type f| /usr/bin/xargs /usr/bin/sha256sum --binary'.format_map(os.environ)
parser = argparse.ArgumentParser(description='Calculate the checksum of remote files to make sure they are not tampered')
parser.add_argument('--mode', action='store', choices=['sum'], required=True, help='Operational modes')
parser.add_argument('--retries', action='store', default=10, help='SSH at Godaddy sucks balls. Be ready to re-try')
parser.add_argument('report', action='store', help='Report destination')
args = parser.parse_args()

client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())
key = paramiko.rsakey.RSAKey.from_private_key_file(CHECKSUM_RSA_KEY_FILE)
attempt = 1
while attempt < args.retries:
    try:
        client.connect(hostname=CHECKSUM_REMOTE_SERVER, pkey=key, banner_timeout=300, timeout=300)
        if args.mode == 'sum':
            print("SSH connected to {0}, getting remote checksums. It will take a while...".format(CHECKSUM_REMOTE_SERVER))
            stdin, stdout, stderr = client.exec_command(REMOTE_CMD)
            with open(args.report, 'w') as rfh:
                for line in stdout.readlines():
                    rfh.write(line)
                    print(line.strip(), file=sys.stdout)
            for line in stderr.readlines():
                print(line.strip(), file=sys.stderr)
    except SSHException:
        wait_time = int(random.uniform(1, 60))
        print("Could not connect, will try again in {0} seconds ({1})".format(wait_time, attempt), file=sys.stdout)
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        time.sleep(wait_time)
        attempt += 1
client.close()
