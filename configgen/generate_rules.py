#!/bin/python
import re

with open("../src/syntax/rule.hpp", 'r') as f:
  one_line = f.read().replace('\n', '')
  matches = re.search(r'RULE_DEFINE_ENUM \*\/(.*)\/\*', one_line)
  enum_string = matches.group(1)
  enum_string = enum_string.replace(",", "\n")
  enum_string = enum_string.replace("smart_enum_class(", "")
  enum_string = re.sub(r'[ \t=0\);]', '', enum_string)
  enum_string = re.sub(r'(.*)', r'  "\1",', enum_string)
  enum_string = "// NOTE: The following is autogenerated \n" +\
    "var ruleNames = [\n" + enum_string + "\n];"
  #print(enum_string)
  
  all_lines = []
  with open("populate.js") as o:
    all_lines = o.readlines()
    begin = end = line_number = 1
    for line in all_lines:
      if "RULE_BEGIN" in line:
        begin = line_number
      if "RULE_END" in line:
        end = line_number
        break
      line_number += 1
    del all_lines[begin:end-1]
    to_append = enum_string.split("\n")[::-1]
    for line in to_append:
      if "RuleType" in line or "Unknown" in line:
        continue
      all_lines.insert(begin, line+"\n")
    print("Script extracted %d rules from cpp (%d lines)" % (len(to_append)-5, len(to_append)))

with open("populate.js", 'w') as o:
  for line in all_lines:
      o.write(line)