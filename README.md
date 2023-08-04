# svn\_git #

About:

covert svn commit since `reversion_number` to now, to git commit.

WARNING:

1.  This will do a `svn cleanup . --remove-unversioned`. Ensure you've ignored git files in `svn` config
2.  Ensure to do a `svn update` before this tool

Usage:
    
```commandline
svn_git <reversion_number>
```

Install:

```commandline
pip install -e .
```