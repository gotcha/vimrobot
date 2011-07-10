import pty


class Controller(object):

    def __init__(self, term, fd):
        self.term = term
        self.fd = fd

    def update(self, timeout=0.1):
        import os
        import select

        fd = self.fd
        readable = []
        while not fd in readable:
            readable, writable, errp = select.select([fd], [], [], 0.01)
        while fd in readable:
            result = os.read(fd, 8192)
            self.term.ProcessInput(result)
            readable, writable, errp = select.select([fd], [], [], timeout)

    @property
    def rows(self):
        return self.term.screen

    def send_keys(self, command):
        import os
        os.write(self.fd, command)


def make_vim():
    pid, fd = pty.fork()
    if pid == 0:
        pty.spawn(['vim', '-u', 'NONE', 'afile.py'])
    else:
        from TermEmulator import V102Terminal
        term = V102Terminal(24, 80)
        vim = Controller(term, fd)
    return vim


def send_command(vim, command):
    print repr(command)
    print '-' * 80
    vim.send_keys(command)


def print_status(vim):
    vim.update()
    for row in vim.rows:
        print row.tostring()
    print '=' * 80


def main():
    vim = make_vim()
    print_status(vim)
    #send_command(vim, ':e afile.py\n')
    #print_status(vim)
    send_command(vim, ':set nocp\n')
    print_status(vim)
    send_command(vim, 'Goabcd')
    print_status(vim)
    send_command(vim, '\x1b:w')
    print_status(vim)
    send_command(vim, '\n')
    print_status(vim)
    send_command(vim, ':q\n')
    print_status(vim)

if __name__ == '__main__':
    main()
