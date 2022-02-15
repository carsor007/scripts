### The UNIX system life cycle Review
Unlike a small computer operating system, the UNIX system is designed to run continuously. Constant operation allows it to schedule tasks a long way in advance, and ensures that the services it provides are available on demand, whenever they are needed. All systems need to be shut down periodically for maintenance, but it is not uncommon for a UnixWare system to run for several weeks or even months between shutdowns.

Whenever you start up a UNIX system, it goes through the following complex life cycle:

### Startup
When you switch a personal computer on, it is not yet ready to run the UNIX system. The machine contains a library of programs stored in read-only memory (or ROM) which are known collectively as the BIOS (or basic input-output system). These programs serve two purposes; they are used by DOS (but not the UNIX system) to access peripheral devices, and they carry out a power-on self-test (or POST) of the computer's hardware.
If all is well, the light on the computer's first floppy disk drive flashes. If a disk containing a small program called a boot program is present in the drive, it will then read the program in and proceed to the next stage; if there is a hardware fault and the POST fails, the computer will either beep a series of tones at you or display a message on its monitor, and refuse to go any further.

### Boot
If the power-on self-test was successful, the boot process commences. The term ``boot'' is a traditional reference to the way in which the system must pull itself up by its own bootstraps, loading a short program that runs and loads a more elaborate program, and so on. The first step in the boot process is for the computer to read in a short program stored in the first sector of either a floppy disk or the first hard drive on the computer. This is carried out by part of the BIOS. The boot sector program then loads another short program, which is just intelligent enough to search the disk for a program called /stand/boot, and read that program into the computer's main memory.
At this stage, the computer is minimally functional. The boot(1M) program cannot make use of virtual memory, mount filesystems, or do any of the other tasks associated with the system; neither can it run under the system when it is operational. What it can do is prompt you for the name of a file to execute, then search the root directory of the root filesystem for that file and load it. To do this it places a prompt on the system console:

[boot]#
and then it waits for you to type the name of the kernel, or any additional instructions that it recognizes. If you do not type anything, it will time out after a specified period and load the default file listed in /etc/default/boot.
Loading the kernel
The kernel is visible on your system as a file in the boot filesystem, called /stand/unix. The boot program copies the kernel into the computer's memory, then starts it running.
When the kernel begins to run, it starts by setting up a number of internal lists, or tables. These tables are used to keep track of running processes, memory allocation, open files, and a number of other things; they are not directly accessible to you. However, two of them which are of interest are the process table (portions of which you can list out with the ps command) and the buffer cache, which is described in ``Understanding filesystems and devices''

After initializing its tables, the kernel creates three dummy processes; sched, pageout and bdflush (with process IDs 0, 2 and 3 respectively). These processes are sections of kernel code which must be called periodically; pageout provides virtual memory paging services, sched provides swapping services, and bdflush flushes the buffer cache periodically. None of these processes can be killed; they are part of the kernel, and are essential to the correct running of the UNIX system.

Finally the kernel creates a third process: init(1M), or process 1. init starts up as a dummy process, then achieves independence: it runs as the first true process on the system. init runs continuously; it is the parent of all other processes on the system.

### Run levels
Run levels define the behavior of init, and by extension those processes which run on the system when it is at any given level. The system starts at run level 0 (shutdown) and then enters run level 1, single user mode. At level 1, only the root filesystem is mounted and only processes connected to the console can run; this means that it is safe to check the unmounted filesystems for integrity without risking any other processes altering them. At other run levels, init starts up the daemon processes that provide various services, and enters multiuser mode.
init executes other programs via the fork system call. Each time init calls fork, it passes control to the kernel, which creates a new entry in the process table, allocates a temporary storage area called a U-area, and copies the calling processes' local data (including the stack) into the U-area. The kernel then returns control to the child process, which may make an exec call, overwriting itself with a new program. init periodically reads a file called /etc/inittab, which tells it which programs to execute at any given run level.

The init(1M) program should not be confused with the init process; the former is an executable program which can be used by the administrator to change the run level of the system or cause the init process to reread the /etc/inittab file.

### Multiuser mode
The Service Access Controller (SAC) daemon is started by init(1M) during system initialization through an entry in /etc/inittab.
It is not uncommon for a system to remain in multiuser mode for days or weeks at a time. However, it is necessary for the system administrator to shut it down for maintenance at regular intervals.

### Shutdown
When the administrator shuts down a system, it follows a set procedure. Because the system may be supporting a number of users, warning messages are broadcast to all terminals before a shutdown. After a short time, init switches to run level 1, killing all the processes linked to terminals and flushing and unmounting all the mounted filesystems. The buffer cache is then flushed (by the sync(1M) program), and the system drops to run level 0, or shutdown.
It is important to understand that unless you are running on a multiprocessor system only one process is actually being executed at any given instant. Although the system is multitasking, a single processor can only carry out one instruction at a time.
The kernel effectively mediates the demands of each process, by scheduling the processes to run one after another. The signal for the kernel to take over is sent by the system clock; every hundredth of a second the kernel wakes up and checks to see if the current process has had its time allocation. If so, the kernel suspends the process and switches execution to the process on the queue with the highest priority.

The kernel also mediates all requests for memory and requests to load and run other processes. The requesting process (be it init or any other process) issues a ``system call'', a request to the kernel to deliver a service; it then suspends execution (sleeps) until the kernel can deliver the requested facility.

The UNIX system provides access to information by mapping it within a notional name space. A name space is simply an abstract space within which all entities are identified by name; items existing in the system name space are files of data (including directories), and special files (such as devices) which provide access to hardware devices such as tapes, terminals or hard disks. Given the name of an entity, the kernel can retrieve it and read its associated data. However, the fact that the entities can all be referred to by the same method should not be confused with equivalence; devices, although they look like files, are not files.
