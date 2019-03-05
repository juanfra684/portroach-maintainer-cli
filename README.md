Portroach CLI client
====================

```plain
$ doas pkg_add python%3 git
$ git clone https://github.com/juanfra684/portroach-maintainer-cli.git
$ cd portroach-maintainer-cli
$ ./outdated-packages.py juanfra@openbsd.org
┌─────────────────────┬─────────┬──────────┐
│         Port        │ OpenBSD │ Upstream │
├─────────────────────┼─────────┼──────────┤
│ archivers/lzip/lzip │    1.15 │     1.16 │
└─────────────────────┴─────────┴──────────┘
$ ./outdated-packages.py -h
usage: outdated-packages.py [-h] [-p | -d] email

positional arguments:
  email        maintainer's email (e.g. maintainer@example.com)

optional arguments:
  -h, --help   show this help message and exit
  -p, --plain  disable the use of utf-8
  -d, --dos    use a DOS style double line to draw the table
```
