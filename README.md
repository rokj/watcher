# watcher

Watcher is simple script for tracking changes of files remotely.

Watching files for changes in:  
| sha512       | ls -al                                                 |  
| ------------ | ------------------------------------------------------ |
| 23kljwgndfkl | -rw-rw-r-- 1 user user 61 Feb 22 12:24 /home/user/test |  


## configuration

Set variables `debug`, `send_mail` and `mail_to` in [`watcher.py`](https://github.com/rokj/watcher/blob/main/watcher.py).  

Set files to watch in `files-to-watch.cfg`. Example in [`files-to-watch.dist.cfg`](https://github.com/rokj/watcher/blob/main/files-to-watch.dist.cfg).

## run

`python3 watcher.py`

Script will track changes and will send email (if set) and write to logfile `watcher.log` if some file from files-to-watch.cfg has changed.

Check watcher.log for changes.

## requirements

- you need to user public key authentication
- you need to have https://linux.die.net/man/1/mailx installed on the system for script to send email when file changed.

