#!/usr/bin/env python3

# Copyright (c) 2014-2020, Juan Francisco Cantero Hurtado <iam@juanfra.info>
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
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "email", help="maintainer's email (e.g. maintainer@example.com)"
)
group_parser = arg_parser.add_mutually_exclusive_group()
group_parser.add_argument(
    "-p", "--plain", help="disable the use of utf-8", action="store_true"
)
group_parser.add_argument(
    "-d",
    "--dos",
    help="use a DOS style double line to draw the table",
    action="store_true",
)
args = arg_parser.parse_args()

portroach_server = "https://portroach.openbsd.org/json/"

# https://en.wikipedia.org/wiki/Box-drawing_character
if args.plain:
    box_left_top = "+"
    box_left_bottom = "+"
    box_right_top = "+"
    box_right_bottom = "+"
    box_middle_top = "+"
    box_middle_bottom = "+"
    box_middle_left = "+"
    box_middle_right = "+"
    box_crux = "+"
    box_line_horizontal = "-"
    box_line_vertical = "|"
    box_line_external_vertical = box_line_vertical
elif args.dos:
    box_left_top = "╔"
    box_left_bottom = "╚"
    box_right_top = "╗"
    box_right_bottom = "╝"
    box_middle_top = "╤"
    box_middle_bottom = "╧"
    box_middle_left = "╠"
    box_middle_right = "╣"
    box_crux = "╪"
    box_line_horizontal = "═"
    box_line_vertical = "│"
    box_line_external_vertical = "║"
else:
    box_left_top = "┌"
    box_left_bottom = "└"
    box_right_top = "┐"
    box_right_bottom = "┘"
    box_middle_top = "┬"
    box_middle_bottom = "┴"
    box_middle_left = "├"
    box_middle_right = "┤"
    box_crux = "┼"
    box_line_horizontal = "─"
    box_line_vertical = "│"
    box_line_external_vertical = box_line_vertical


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
            box_left_top
            + (box_line_horizontal * (size_1column + 2))
            + box_middle_top
            + (box_line_horizontal * (size_2column + 2))
            + box_middle_top
            + (box_line_horizontal * (size_3column + 2))
            + box_right_top
        )
    elif position == "middle":
        print(
            box_middle_left
            + (box_line_horizontal * (size_1column + 2))
            + box_crux
            + (box_line_horizontal * (size_2column + 2))
            + box_crux
            + (box_line_horizontal * (size_3column + 2))
            + box_middle_right
        )
    elif position == "bottom":
        print(
            box_left_bottom
            + (box_line_horizontal * (size_1column + 2))
            + box_middle_bottom
            + (box_line_horizontal * (size_2column + 2))
            + box_middle_bottom
            + (box_line_horizontal * (size_3column + 2))
            + box_right_bottom
        )


def headers_box():
    lines_box("top")
    print(
        box_line_external_vertical
        + title_1column.center(size_1column + 2)
        + box_line_vertical
        + title_2column.center(size_2column + 2)
        + box_line_vertical
        + title_3column.center(size_3column + 2)
        + box_line_external_vertical
    )


def generate_table(maintained_ports):
    global size_1column, size_2column, size_3column

    for port in maintained_ports:
        if port["newver"]:
            if len(port["cat"]) + len(port["name"]) + 1 > size_1column:
                size_1column = len(port["cat"]) + len(port["name"]) + 1
            if len(port["ver"]) > size_2column:
                size_2column = len(port["ver"])
            if len(port["newver"]) > size_3column:
                size_3column = len(port["newver"])

    headers_box()
    for port in maintained_ports:
        if port["newver"]:
            lines_box("middle")
            print(
                box_line_external_vertical
                + " "
                + (port["cat"] + "/" + port["name"]).ljust(size_1column + 1)
                + box_line_vertical
                + port["ver"].rjust(size_2column + 1)
                + " "
                + box_line_vertical
                + port["newver"].rjust(size_3column + 1)
                + " "
                + box_line_external_vertical
            )
    lines_box("bottom")


maintainers = json_request("totals")["results"]
maintainers_found = [
    maintainer["maintainer"]
    for maintainer in maintainers
    if args.email in maintainer["maintainer"]
]

if len(maintainers_found) == 0:
    sys.exit('"' + args.email + '"' + " was not found in the server.")
else:
    maintainers_group = []
    for maintainer_entry in maintainers_found:
        if maintainer_entry.count("@") == 1:
            generate_table(json_request(maintainer_entry))
        else:
            maintainers_group.extend(json_request(maintainer_entry))
    if len(maintainers_group) != 0:
        print("\nPorts maintained with others")
        generate_table(maintainers_group)
