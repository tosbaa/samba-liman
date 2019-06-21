import os
import subprocess

proc = subprocess.Popen("getfacl ACL", shell=True, stdout=subprocess.PIPE)
output_string = proc.stdout.read()
print(output_string.split("\n"))