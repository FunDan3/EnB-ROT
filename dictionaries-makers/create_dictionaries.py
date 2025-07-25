#! /usr/bin/python3
import os, subprocess, shutil

targets = filter(lambda path: os.path.isdir(f"./{path}"), os.listdir("./"))
root_path = os.getcwd()
term_columns, term_rows = shutil.get_terminal_size()
for target in targets:
	print(f" {target.upper()} ".center(term_columns, "="))
	os.chdir(f"./{target}/")
	if os.path.exists(f"./__source-dict__"):
		subprocess.run(["rm", f"./__source-dict__/", "-rf"])
	subprocess.run(["./download_source.sh"])
	subprocess.run(["./conv.py"])
	os.chdir(root_path)
