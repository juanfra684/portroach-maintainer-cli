#!/usr/bin/env python3.4

# Copyright (c) 2014, Juan Francisco Cantero Hurtado <iam@juanfra.info>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import urllib.request
import urllib.parse
import json
import sys

if len(sys.argv) == 1:
    sys.exit(1)

portroach_server = "http://ftp.fr.openbsd.org/portscout/json/"

def json_request(json_file):
    portroach_json = portroach_server + json_file + ".json"
    portroach_data = urllib.request.urlopen(portroach_json).read().decode("utf8")
    portroach_dict = json.loads(portroach_data)
    return portroach_dict

for i in json_request("totals"):
    if sys.argv[1] in i["maintainer"]:
        for ii in json_request(i["maintainer"]):
            if ii["newver"] != None:
                print (ii["name"], ii["newver"], ii["ver"])

