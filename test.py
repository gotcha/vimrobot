import pty


class ControledVim(object):

    def __init__(self, term, fd):
        self.term = term
        self.fd = fd

    def readToTerminal(self, timeout=0.1):
        import os
        import select

        fd = self.fd
        readable = []
        while not fd in readable:
            readable, writable, errp = select.select([fd], [], [], 0.01)
        while fd in readable:
            result = os.read(fd, 8192)
            term.ProcessInput(result)
            readable, writable, errp = select.select([fd], [], [], timeout)
        rows = self.term.screen
        for row in rows:
            print row.tostring()
        print '=' * 80

    def sendToVim(self, command):
        import os
        print repr(command)
        print '-' * 80
        os.write(self.fd, command)


pid, fd = pty.fork()
if pid == 0:
    pty.spawn(['vim', '-u', 'NONE', 'afile.py'])
else:
    from TermEmulator import V102Terminal
    term = V102Terminal(24, 80)
    vim = ControledVim(term, fd)
    vim.readToTerminal()
    #vim.sendToVim(':e afile.py\n')
    #vim.readToTerminal()
    vim.sendToVim(':set nocp\n')
    vim.readToTerminal()
    vim.sendToVim('Goabcd')
    vim.readToTerminal()
    vim.sendToVim('\x1b:w')
    vim.readToTerminal()
    vim.sendToVim('\n')
    vim.readToTerminal()
    vim.sendToVim(':q\n')
    vim.readToTerminal()
