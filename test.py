import pty


def readToTerminal(term, fd, timeout=0.1):
    import os
    import select
    readable = []
    while not fd in readable:
        readable, writable, errp = select.select([fd], [], [], 0.01)
    while fd in readable:
        result = os.read(fd, 8192)
        term.ProcessInput(result)
        readable, writable, errp = select.select([fd], [], [], timeout)
    rows = term.screen
    for row in rows:
        print row.tostring()
    print '=' * 80


def sendToVim(fd, command):
    import os
#    readable, writable, errp = select.select([fd], [fd], [])
#    while fd not in writable:
#        readable, writable, errp = select.select([fd], [fd], [])
    print repr(command)
    print '-' * 80
    os.write(fd, command)

pid, fd = pty.fork()
if pid == 0:
    pty.spawn(['vim'])
else:
    from TermEmulator import V102Terminal
    term = V102Terminal(24, 80)
    readToTerminal(term, fd)
    sendToVim(fd, ':e bla.txt\n')
    readToTerminal(term, fd)
    sendToVim(fd, 'Goabcd')
    readToTerminal(term, fd)
    sendToVim(fd, '\x1b:w')
    readToTerminal(term, fd)
    sendToVim(fd, '\n')
    readToTerminal(term, fd)
    sendToVim(fd, ':q\n')
    readToTerminal(term, fd)
