"""
Usage:
    svn_git [Options] [--reversion=<target_svn_revision>] [--timezone=<timezone>]

Options:
    -r, --reversion=<target_svn_revision>  target svn reversion [default: local_last_svn_reversion]
    -t, --timezone=<timezone>              timezone [default: system_local_timezone]
"""
import subprocess
import sys
from datetime import datetime
import pysvn
import pytz
import docpie
from tzlocal import get_localzone

def main():

    args = dict(docpie.docpie(__doc__))

    local_repo_path = '.'

    target_svn_revision: int
    if args['--reversion'] != 'local_last_svn_reversion':
        target_svn_revision = int(args['--reversion'])
        print(f'using revision {target_svn_revision}')
    else:
        svn_client = pysvn.Client()
        log_entries = svn_client.log(local_repo_path)
        target_svn_revision = log_entries[0]['revision']
        subprocess.run(['svn', 'cleanup', '.', '--remove-unversioned'], check=True)
        subprocess.run(['svn', 'update'], check=True)
        print(f'using latest revision {target_svn_revision}')

    svn_client = pysvn.Client()
    log_entries = svn_client.log(local_repo_path)

    # Iterate through the log entries to access commit information
    new_svn_log = []

    for log_entry in log_entries:
        # print(log_entry)
        if log_entry['revision'] == target_svn_revision:
            print(f'found: {log_entry}')
            break

        new_svn_log.append(log_entry)
        # Access commit information
        # commit_revision = log_entry.revision.number
        # author = log_entry.author
        # commit_date = log_entry.date
        # commit_message = log_entry.message

        # Do whatever you want with the commit information
        # print(f"Revision: {commit_revision}")
        # print(f"Author: {author}")
        # print(f"Date: {commit_date}")
        # print(f"Message: {commit_message}")
        # print("-" * 50)
    else:
        print(f'no svn log found {target_svn_revision}')

    subprocess.run(['svn', 'cleanup', '.', '--remove-unversioned'], check=True)
    # 将新的 svn commit, 喂给 git
    local_timezone = pytz.timezone('Asia/Shanghai')
    if args['--timezone'] == 'system_local_timezone':
        local_timezone = get_localzone()
    else:
        local_timezone = pytz.timezone(args['--timezone'])

    print(f'using timezone {local_timezone}')

    for svn_log in new_svn_log[::-1]:
        svn_reversion = svn_log['revision']
        svn_datetime_str = svn_log['date']

        subprocess.run(['svn', 'update', '-r', str(svn_reversion), '--set-depth', 'infinity'], check=True)
        subprocess.run(['svn', 'cleanup', '.', '--remove-unversioned'], check=True)
        print(svn_log)
        # input(f'{svn_reversion} {svn_datetime_str}: enter to continue...')

        # git_datetime_str = svn_datetime_str.split('.')[0].replace('T', ' ')  # + ' +0800'
        svn_format_string = "%Y-%m-%dT%H:%M:%S.%fZ"
        commit_datetime = datetime.strptime(svn_datetime_str, svn_format_string).replace(tzinfo=pytz.UTC)
        tz_commit_datetime = commit_datetime.astimezone(local_timezone)
        zone_format_string = "%Y-%m-%d %H:%M:%S.%f %z"
        git_datetime_str = tz_commit_datetime.strftime(zone_format_string)

        # git_datetime_str = svn_datetime_str.split('.')[0].replace('T', ' ').replace('Z', '') + ' +0000'
        # print(git_datetime_str)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', f'[svn:{svn_reversion}:{svn_log["author"]}]{svn_log["msg"] or ""}', '--date', git_datetime_str], check=True)


if __name__ == '__main__':
    main()
