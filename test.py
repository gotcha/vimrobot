import pty


def readToTerminal(vim, timeout=0.1):
    import os
    import select

    fd = vim.fd
    term = vim.term

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


def sendToVim(vim, command):
    import os
    print repr(command)
    print '-' * 80
    os.write(vim.fd, command)


class ControledVim(object):

    def __init__(self, term, fd):
        self.term = term
        self.fd = fd

pid, fd = pty.fork()
if pid == 0:
    pty.spawn(['vim', '-u', 'NONE', 'afile.py'])
else:
    from TermEmulator import V102Terminal
    term = V102Terminal(24, 80)
    vim = ControledVim(term, fd)
    readToTerminal(vim)
    #sendToVim(vim, ':e afile.py\n')
    #readToTerminal(vim)
    sendToVim(vim, ':set nocp\n')
    readToTerminal(vim)
    sendToVim(vim, 'Goabcd')
    readToTerminal(vim)
    sendToVim(vim, '\x1b:w')
    readToTerminal(vim)
    sendToVim(vim, '\n')
    readToTerminal(vim)
    sendToVim(vim, ':q\n')
    readToTerminal(vim)
