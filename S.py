# Attempt 1: 
# import subprocess, sys
# from shlex import split
# cmd = split("ffmpeg -h")
 
# ## run it ##
# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
 
# while True:
#     print(p.poll())

# ## But do not wait till netstat finish, start displaying output immediately ##
# while True:
#     out = p.stderr.read(1).decode()
#     if out == b'' and p.poll() != None:
#         break
#     if out != b'':
#         print(out, end='')
#         #sys.stdout.write(out.decode())
#         #sys.stdout.flush()

# while True:
#     out = p.stdout.read(1).decode()
#     if out == b'' and p.poll() != None:
#         break
#     if out != b'':
#         print(out, end='')
#         #sys.stdout.write(out.decode())
#         #sys.stdout.flush()

# attempt 2:
# while simpler, it still does not work (it does not recognize the program closing, and runs forever (specificlaly the case with ffmpeg -h, not ffmpeg, but multiple other commands too))
import os
x=os.popen("ffmpeg -h")
