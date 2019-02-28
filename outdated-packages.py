#!/usr/bin/env python3

# Copyright (c) 2019, Juan Francisco Cantero Hurtado <iam@juanfra.info>
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
    print(f"usage: {sys.argv[0]} maintainer@example.com", file=sys.stderr)
    sys.exit(1)

portroach_server = "http://portroach.openbsd.org/json/"

# https://en.wikipedia.org/wiki/Box-drawing_character
uni_left_top = "\u250C"
uni_left_bottom = "\u2514"
uni_right_top = "\u2510"
uni_right_bottom = "\u2518"
uni_middle_top = "\u252C"
uni_middle_bottom = "\u2534"
uni_middle_left = "\u251C"
uni_middle_right = "\u2524"
uni_crux = "\u253C"
uni_line_horizontal = "\u2500"
uni_line_vertical = "\u2502"

title_1column = "Port"
title_2column = "OpenBSD"
title_3column = "Upstream"

size_1column = len(title_1column)
size_2column = len(title_2column)
size_3column = len(title_3column)


def json_request(json_file):
    portroach_json = portroach_server + urllib.parse.quote(json_file) + ".json"
    portroach_data = (
        urllib.request.urlopen(portroach_json).read().decode("utf8")
    )
    portroach_dict = json.loads(portroach_data)
    return portroach_dict


def lines_box(position):
    if position == "top":
        print(
            uni_left_top
            + (uni_line_horizontal * (size_1column + 2))
            + uni_middle_top
            + (uni_line_horizontal * (size_2column + 2))
            + uni_middle_top
            + (uni_line_horizontal * (size_3column + 2))
            + uni_right_top
        )
    elif position == "middle":
        print(
            uni_middle_left
            + (uni_line_horizontal * (size_1column + 2))
            + uni_crux
            + (uni_line_horizontal * (size_2column + 2))
            + uni_crux
            + (uni_line_horizontal * (size_3column + 2))
            + uni_middle_right
        )
    elif position == "bottom":
        print(
            uni_left_bottom
            + (uni_line_horizontal * (size_1column + 2))
            + uni_middle_bottom
            + (uni_line_horizontal * (size_2column + 2))
            + uni_middle_bottom
            + (uni_line_horizontal * (size_3column + 2))
            + uni_right_bottom
        )


def headers_box():
    lines_box("top")
    print(
        uni_line_vertical
        + title_1column.center(size_1column + 2)
        + uni_line_vertical
        + title_2column.center(size_2column + 2)
        + uni_line_vertical
        + title_3column.center(size_3column + 2)
        + uni_line_vertical
    )


for i in json_request("totals")["results"]:
    if sys.argv[1] in i["maintainer"]:
        results_maintainer = json_request(i["maintainer"])
        for ii in results_maintainer:
            if ii["newver"] != None:
                if len(ii["cat"]) + len(ii["name"]) + 1 > size_1column:
                    size_1column = len(ii["cat"]) + len(ii["name"]) + 1
                if len(ii["ver"]) > size_2column:
                    size_2column = len(ii["ver"])
                if len(ii["newver"]) > size_3column:
                    size_3column = len(ii["newver"])

        headers_box()
        for ii in results_maintainer:
            if ii["newver"] != None:
                lines_box("middle")
                print(
                    uni_line_vertical
                    + " "
                    + (ii["cat"] + "/" + ii["name"]).ljust(size_1column + 1)
                    + uni_line_vertical
                    + ii["ver"].rjust(size_2column + 1)
                    + " "
                    + uni_line_vertical
                    + ii["newver"].rjust(size_3column + 1)
                    + " "
                    + uni_line_vertical
                )
        lines_box("bottom")
        break
