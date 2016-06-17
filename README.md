Portroach CLI client
====================

```sh
$ doas pkg_add python%3.5 git
$ git clone https://gitlab.com/juanfra684/portroach-maintainer-cli.git
$ cd portroach-maintainer-cli
$ ./outdated-packages.py juanfra@openbsd.org
┌─────────────────────┬─────────┬──────────┐
│         Port        │ OpenBSD │ Upstream │
├─────────────────────┼─────────┼──────────┤
│ archivers/lzip/lzip │    1.15 │     1.16 │
└─────────────────────┴─────────┴──────────┘
```