#! /usr/bin/python -B
# -*-coding:utf-8 -*

import sys
import os
import re
from color import Color

def print_error(string):
    print(Color.RED + string + Color.DEFAULT)

def print_line(nb, line):
    nb += 1
    print(Color.PINK + "Line " + str(nb) + " : " + Color.DEFAULT + line)

def check_regex(regex, msg_error, nb, line):
    if re.search(regex, line) is not None:
        print_error(msg_error)
        print_line(nb, line)

def check_file(nb, line):
    tab_regex = [
        (".{79,}", "Exceed 80 characters in width : "),
        ("^.+#.*", "'#' must appear on the first column : "),
        ("^#\s*if(def|ndef)?[A-Z0-9_]", "'#if' and '#ifdef’ MUST be indented by one character : "),
        ("^#\s*(else|endif)\s*$", "'#else' and '#endif' MUST be followed by a comment : "),
        ("(if|while|for|sizeof|elseif|switch|return)\(", "Need a space between keyword and '(' : "),
        ("throw\s*\(", "MUST NOT put parenthesis after a throw : "),
        ("(do|if|typeid|sizeof|case|catch|switch|template|for|throw|while|try)[^ ]\(", "Need a space after a keyword :"),
        ("(if|while|for|elseif|switch|else|do|try).*{.*", "All braces MUST be on their own lines : "),
        ("(int|char|void|long|float|double|size_t|short).*,.*;", "One field declaration per line : "),
        ("((=|\+|-|/)[^ =!<>+]|[^ =!<>+](=|\+|-|/))", "Need a whitespace after a operator : "),
        ("(int|char|void|long|float|double|size_t|short)\s+\*", "Pointor not initialized correctly : "),
        ("[^ (]\(", "Almost all parentheses must be preceded by a whitespace : "),
        (".*,[^ ].*", "The comma MUST be followed by a single space : "),
        ("\(void\)", "Functions _MUST NOT_ take a 'void' argument : "),
        ("return \(", "'return' MUST NOT be enclosed in parenthesis : "),
        ("\S\s+$", "Trailing whitespace : "),
        ("operator(\,|\|\||&&|&)", "MUST NOT overload : "),
        ("template<", "MUST leave one space between template : "),
    ]

    for regex, msg_error in tab_regex:
        check_regex(regex, msg_error, nb, line)

print("\nC++11 Coding Style Standard\n")

if len(sys.argv) > 1:
    print("Directory opened : " + sys.argv[1] + "\n")
    print("----------------------------------------\n")
else:
    print(Color.RED + "Please specify a location !" + Color.DEFAULT)
    sys.exit(1)

if sys.argv[1] == ".":
    sys.argv[1] += "/"

if sys.argv[1][-1:] != "/":
    sys.argv[1] += "/"

for filename in sorted(os.listdir(sys.argv[1])):
    filename = sys.argv[1] + filename
    extension = os.path.splitext(filename)[1]

    if os.path.isfile(filename) and (extension == ".cc"
                                     or extension == ".hh"
                                     or extension == ".hxx"):
        with open(filename, "r") as file:
            print("Filename : " + Color.BLUE + filename + Color.DEFAULT)

            lines = file.read().splitlines()

            for nb, line in enumerate(lines):
                check_file(nb, line)

            print
