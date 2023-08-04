import subprocess
import pysvn
import sys


def main():
    # # Replace 'path_to_repo' with the path to your local Git repository
    # repo = git.Repo('.')
    #
    # # Get the reference to the head commit (most recent commit in the current branch)
    # head_commit = repo.head.commit
    #
    # git_commit_target_hash = '7bfcc096803218ff6f4c53be9f7939a378b4ba4e'
    # svn_merge_commit: Commit | None = None
    #
    # # Iterate through the commit history starting from the head commit
    # # for commit in itertools.islice(repo.iter_commits(head_commit), 2):
    # for commit in repo.iter_commits(head_commit):
    #     # Access commit information
    #     commit_hash = commit.hexsha
    #     author_name = commit.author.name
    #     author_email = commit.author.email
    #     commit_date = commit.authored_datetime
    #     commit_message = commit.message
    #
    #     # Do whatever you want with the commit information
    #     print(f"Commit Hash: {commit_hash}")
    #     print(f"Author: {author_name} <{author_email}>")
    #     print(f"Date: {commit_date}")
    #     print(f"Message: {commit_message}")
    #     print("-" * 50)
    #
    #     if commit_hash == git_commit_target_hash:
    #         svn_merge_commit = commit
    #         break
    # else:
    #     assert False, "commit not found"
    #
    # print(f'found commit: {svn_merge_commit}')

    local_repo_path = '.'

    # Initialize the SVN client
    svn_client = pysvn.Client()

    # Get the commit history using 'svn log'
    log_entries = svn_client.log(local_repo_path)

    # target_svn_revision: int = 1339
    target_svn_revision: int = int(sys.argv[1])

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
    for svn_log in new_svn_log[::-1]:
        svn_reversion = svn_log['revision']
        svn_datetime_str = svn_log['date']

        subprocess.run(['svn', 'update', '-r', str(svn_reversion), '--set-depth', 'infinity'], check=True)
        subprocess.run(['svn', 'cleanup', '.', '--remove-unversioned'], check=True)
        print(svn_log)
        input(f'{svn_reversion} {svn_datetime_str}: enter to continue...')

        git_datetime_str = svn_datetime_str.split('.')[0].replace('T', ' ') + ' +0800'
        # print(git_datetime_str)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', f'[svn:{svn_log["author"]}]{svn_log["msg"] or ""}', '--date', git_datetime_str], check=True)
        input(f'git {git_datetime_str}: enter to continue...')


if __name__ == '__main__':
    main()