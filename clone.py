import signal, ctypes, os

libc = ctypes.CDLL('libc.so.6', use_errno=True)
CLONE_NEWPID = 0x20000000
CLONE_NEWUSER = 0x10000000
stack = ctypes.byref(ctypes.create_string_buffer(0x200000), 0x200000)

CHILDFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
@CHILDFUNC
def childfunc(_):
    print("CHILD", "pid:", os.getpid(), "uid:", os.getuid())
    return 0

pid = libc.clone(childfunc, stack,
    CLONE_NEWPID|CLONE_NEWUSER|signal.SIGCHLD, 0)
assert pid > 0, "Clone error: " + os.strerror(ctypes.get_errno())
print("PARENT", "pid:", os.getpid(), "uid:", os.getuid(), "child:", pid)
os.waitpid(pid, 0)
