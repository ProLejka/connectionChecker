# connectionChecker

## Description

Small project in python that checks internet connection by pinging sites. When site is unreachable it write it into sqlite database for later to analyze.

## Usage

You can run it manually or install service located in `service` directory

## Sitemanager

Included sitemanager.

List sites:

```./sitemanager.py list```

Add site(s):

```./sitemanager.py add SITE1 SITE2...```

or

```./sitemanager.py SITE1 SITE2...```

Remove site(s):

```./sitemanager.py remove SITE1 SITE2...```