#!/usr/bin/env python

import sys, os, re

# begin loop:
# - reading from stdin
# - forking a child
# - executing a new process in the child

def main():
	while True:
		sys.stdout.write(os.environ['PROMPT'])
		line = sys.stdin.readline()

		commands = split_on_pipes(line)
		placeholder_in = sys.stdin
		placeholder_out = sys.stdout
		pipe = []
		pids = []

		for line in commands:
			args = line.split()
			command = args[0]

			if command in BUILTINS:
				# run built-in instead of doing fork + exec
				run_builtin(command, args)
			else:
				# if command is not the last command
				if (commands.index(line) + 1) < len(commands):
					pipe = os.pipe() # file descriptors
					placeholder_out = pipe[1]
				else:
					placeholder_out = sys.stdout

				pid = fork_and_exec(command, args, placeholder_out, placeholder_in)
				pids.append(pid)

				if type(placeholder_out) is int:
					os.close(placeholder_out)

				if type(placeholder_in) is int:
					os.close(placeholder_in)

				if commands.index(line) > 0:
					placeholder_in = pipe[0]

		for id in pids:
			wait_for_child(id)

def wait_for_child(pid):
	try:
		os.waitpid(pid, 0)
	except:
		None	

# returns PID of child process
def fork_and_exec(command, args, placeholder_out, placeholder_in):
	pid = os.fork()
	if pid == 0: # inside child process
		if type(placeholder_out) is int:
			sys.stdout = os.fdopen(placeholder_out, 'w')
			os.close(placeholder_out)

		if type(placeholder_in) is int:
			sys.stdin = os.fdopen(placeholder_in, 'r')
			os.close(placeholder_in)

		try:
			os.execvp(command, args) # actual exec
		except:
			print "Error: command not found."
	return pid


def run_builtin(command, args):
	try:
		BUILTINS[command](args[1])
	except:
		BUILTINS[command]()

# returns an array of command strings
def split_on_pipes(line):
	matches = re.findall("([^\"'|]+)|[\"']([^\"']+)[\"']", line)
	commands = []
	for match in matches:
		for string in match:
			if string != '':
				commands.append(string.strip())
	return commands

def set(args):
  key, value = args.split('=')
  os.environ[key] = value

BUILTINS = {
	'cd': lambda path: os.chdir(''.join(path)),
	'exit': lambda exit_code=0: sys.exit(int(exit_code)),
	'set': lambda args: set(args) # can't do variable assignment in Python lambda
}

os.environ['PROMPT'] = "=> "

main()
