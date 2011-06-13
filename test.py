import pty


def readToTerminal(term, fd):
    import os
    import select
    readable, writable, errp = select.select([fd], [fd], [])
    while fd in readable:
        result = os.read(fd, 8192)
        term.ProcessInput(result)
        readable, writable, errp = select.select([fd], [fd], [])
    rows = term.screen
    for row in rows:
        print row.tostring()
    print '-'*80

def sendToVim(fd, command):
    import os
#    readable, writable, errp = select.select([fd], [fd], [])
#    while fd not in writable:
#        readable, writable, errp = select.select([fd], [fd], [])
    print repr(command)
    print '-'*80
    os.write(fd, command)
    time.sleep(.2)

pid, fd = pty.fork()
if pid == 0:
    pty.spawn('vim')
else:
    import time
    time.sleep(.2)
    from TermEmulator import V102Terminal
    term = V102Terminal(24, 80)
    readToTerminal(term, fd)
    sendToVim(fd, ':e bla.txt\n')
    readToTerminal(term, fd)
    sendToVim(fd, 'oabcd')
    readToTerminal(term, fd)
    sendToVim(fd, '\x1b:wq\n')
    readToTerminal(term, fd)
