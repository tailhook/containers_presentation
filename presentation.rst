:css: my.css

.. title:: Linux Containers Ecosystem

----

==========================
Linux Containers Ecosystem
==========================

----

:data-scale: 2
:data-x: 500
:data-y: 0

----

:data-x: 1000
:data-y: -500
:data-scale: 1

Internals
+++++++++

----

:data-x: r2000

Process Management
==================

----

The most obvious way:

.. code-block:: python

   proc = subprocess.Popen(...)
   proc.wait()


----

Low level API:

.. code-block:: python

    pid = os.spawnve(os.P_NOWAIT, ...)
    os.waitpid(pid, 0)

----

Even more low level:

.. code-block:: python

    pid = os.fork()
    if pid == 0:
        os.execve(...)
    assert pid > 0, "Fork failed"
    os.waitpid(pid, 0)


----

``fork()`` at system call level (``strace``)::

    clone(child_stack=0,
        flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD,
        child_tidptr=0x7fcd0e8539d0) = 8697

----

Finally namespaces (bad example!):

.. code-block:: python
    :class: part1

    import signal, ctypes, os

    libc = ctypes.CDLL('libc.so.6', use_errno=True)
    CLONE_NEWPID = 0x20000000
    CLONE_NEWUSER = 0x10000000
    stack = ctypes.byref(ctypes.create_string_buffer(0x200000), 0x200000)

.. code-block:: python
    :class: part2

    CHILDFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
    @CHILDFUNC
    def childfunc(_):
        print("CHILD", "pid:", os.getpid(), "uid:", os.getuid())
        return 0

.. code-block:: python
    :class: part3

    pid = libc.clone(childfunc, stack,
        CLONE_NEWPID|CLONE_NEWUSER|signal.SIGCHLD, 0)
    assert pid > 0, "Clone error"
    print("PARENT", "pid:", os.getpid(),
        "uid:", os.getuid(), "child:", pid)
    os.waitpid(pid, 0)

----

:id: clone_part1
:data-x: r100
:data-y: r-50
:data-scale: 0.7

----

:id: clone_part2
:data-x: r0
:data-y: r100

----

:id: clone_part3
:data-x: r0
:data-y: r150

----

:data-x: r2000
:data-scale: 1

Output (the order of lines is arbitrary)::

    $ python3 clone.py
    PARENT pid: 14305 uid: 1000 child: 14306
    CHILD pid: 1 uid: 65534

----

Namespaces:

* CLONE_NEWIPC
* CLONE_NEWNET
* CLONE_NEWNS
* CLONE_NEWPID
* CLONE_NEWUTS
* CLONE_NEWUSER

----

But there is ``chroot`` since 1993!

----

:id: fs_table

+--------------------------+----------+
|/var/lib/lxc/ubuntu/rootfs|          |
+--------------------------+----------+
|                          | * /usr   |
|                          | * /var   |
|                          | * /dev   |
|                          | * ...    |
+--------------------------+----------+
|/var/lib/lxc/nix/rootfs   |          |
+--------------------------+----------+
|                          | * /nix   |
|                          | * /run   |
|                          | * ...    |
+--------------------------+----------+

----

With root privileges you can just:

.. code-block:: python

   os.chroot('/var/lib/lxc/ubuntu/rootfs')

----

CLONE_NEWNS
===========

mount namespaces

available in 2.4.19 (2003)

----

``mount --bind``

available in 2.4.0 (2001)

----

Create hierarchy in new mount namespace:

.. code-block:: bash

    mount --bind /var/lib/lxc/ubuntu/rootfs \
                 /usr/lib/lxc/rootfs
    mount --bind /dev \
                 /usr/lib/lxc/rootfs/dev
    mount -t tmpfs tmpfs /usr/lib/lxc/rootfs/tmp
    # note /var/lib/lxc/ubuntu/rootfs/{dev,tmp} still empty
    chroot /usr/lib/lxc/rootfs bash

----

CLONE_NEWPID
============

* own pid 1
* ``KILL``'ed when pid 1 dead
* separate ``/proc``

----

CLONE_NEWIPC
============

* semaphores
* message queues
* etc.

----

CLONE_NEWUTS
============

* ``hostname``

----

CLONE_NEWNET
============

* network interfaces
* iptables rules
* localhost

-----

CLONE_NEWNET
============

useful on its own using ``ip netns``

-----

CLONE_NEWUSER
=============

containers by unprivileged users

----

:data-scale: 2
:data-x: 500
:data-y: 0

----

:data-x: 1000
:data-y: 0
:data-scale: 1

Tools
+++++

----

:data-x: r2000

Docker
======

----

LXC
===

----

Vagrant-LXC
===========

----

Vagga
=====

----

:data-scale: 2
:data-x: 500
:data-y: 0

----

:data-scale: 1
:data-x: 1000
:data-y: 500

Security
++++++++

----

:data-x: r2000

Running as Root
===============

----

Root in LXC
-----------

* ``+`` setuid

----

Root in Docker
--------------

* ``+`` setuid (?)

----

Root in User Namespace
----------------------

----

Docker Socket
=============

----

SkyDNS
------

----

Docker Socket With Mesos
------------------------

----

... + Mesosphere
----------------


----

Docker Images
-------------

