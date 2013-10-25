# Shy

A basic Unix shell written in Python, based on [Shirt](https://github.com/jstorimer/shirt/tree/fourth).

Try it:

```bash
$ chmod +x shy.py
$ ./shy.py
```

#### Note:
Because Python appears to [reset the STDIN/STDOUT streams of a process executed by os.exec*()](http://docs.python.org/2.7/library/sys.html#sys.stdout), piping is broken and will use STDIN/STDOUT to get its input/output instead of the readable/writable ends of a pipe. Let me know if there's a solution to this.

See LICENSE