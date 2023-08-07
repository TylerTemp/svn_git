# svn\_git #

About:

covert svn commit since `reversion_number` to now, to git commit.

WARNING:

1.  This will do a `svn cleanup . --remove-unversioned`. Ensure you've ignored git files in `svn` config
2.  Ensure to do a `svn update` before this tool

Usage:

```
Usage:
    svn_git [Options] [--reversion=<target_svn_revision>] [--timezone=<timezone>]

Options:
    -r, --reversion=<target_svn_revision>  target svn reversion [default: local_last_svn_reversion]
    -t, --timezone=<timezone>              timezone [default: system_local_timezone]
```

If omit `reversion_number`, it will use the latest local commit reversion, then do `svn cleanup` & `svn update`

Install:

```bash
pip install -e .
```