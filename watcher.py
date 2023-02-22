import json
import os.path
import subprocess
from subprocess import PIPE, CalledProcessError
import datetime
import sys

debug = False
send_mail = False
mail_to  = ""


def run_cmd(command):
    global debug

    if debug:
        print("doing command: {1}".format(remote, command))

    p = subprocess.run(command, shell=True)
    if p.returncode != 0:
        print("failed to execute command >>{0}<<".format(command))


def run_rcmd(remote, command):
    global debug

    print("doing check on >>{0}<< command >>{1}<<".format(remote, command))

    p = subprocess.check_output("ssh -o PubkeyAuthentication=yes -o PreferredAuthentications=publickey {0} \"{1}\"".format(remote, command), shell=True)
    output = p.decode("utf-8").replace("\n", "")
    if debug:
        print("|{0}|".format(output))

    return output

if not os.path.isfile("files-to-watch.cfg"):
    print("does config file files-to-watch.cfg exists? check files-to-watch.dist.cfg for an example")
    sys.exit(1)

if not os.path.isfile("db.json"):
    if debug:
        print("creating db file")
    db = {}
else:
    f = open ('db.json', "r")
    db = json.loads(f.read())

lines = []
with open("files-to-watch.cfg") as f:
    for line in f:
        if line.startswith("#"):
            continue
        lines.append(line.strip())

changed_files = []

for l in lines:
    remote, file = l.split(":") 
    
    try:
        sha = run_rcmd(remote, "sha512sum {0} | cut -d' ' -f1".format(file))
    except CalledProcessError as e:
        changed_files.append("warning: cannot execute command >>{0}<<".format(l))
        continue

    if not l in db:
        db[l] = {"history": []}
    
    db[l]["history"].append({"datetime": "{0}".format(datetime.datetime.now()), "sha512": "{0}".format(sha), "ls": "{0}".format(ls)})
    
    if len(db[l]["history"]) > 1 and (
        db[l]["history"][-1]["sha512"] != db[l]["history"][-2]["sha512"] or 
        db[l]["history"][-1]["ls"] != db[l]["history"][-2]["ls"]
    ):
        changed_files.append("warning: file >>{0}<< changed".format(l))


with open("db.json", 'w') as f:
    json.dump(db, f, ensure_ascii=False, indent=4)
        
if len(changed_files) > 0:
    s = "\n".join(changed_files)
    run_cmd("echo \"{0}\" >> watcher.log".format(s))
    if send_mail:
        s = " ".join(changed_files)
        run_cmd("echo \"{1}\" | mail -s \"files changed\" {0}".format(mail_to, s))

