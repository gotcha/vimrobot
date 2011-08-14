class Controller(object):

    def __init__(self, term, fd, child):
        self.term = term
        self.fd = fd
        self.child = child

    def stop(self):
        import os
        os.kill(self.child, 9)

    def updated(self, timeout=0.01):
        import os
        import select

        fd = self.fd
        readable, writable, errp = select.select([fd], [], [], timeout)
        updated = False
        if fd in readable:
            bytes_read = os.read(fd, 1024)
            updated = bool(bytes_read)
            if updated:
                self.term.ProcessInput(bytes_read)
            else:
                print 'not updated'
        return updated

    @property
    def rows(self):
        return self.term.screen

    def send_keys(self, command):
        import os
        os.write(self.fd, command)

    def get_screen(self):
        result = []
        for index, row in enumerate(self.rows):
            result.append(self.format_row(index, row))
        screen = '\n'.join(result)
        return screen

    def format_row(self, index, row):
        return '%02d %s' % (index, row.tostring())


def make(vim_command='vim', rcfiles=[], files_to_edit=[]):
    import pty

    pid, fd = pty.fork()

    if pid != 0:  # parent process emulates terminal
        from TermEmulator import V102Terminal
        term = V102Terminal(24, 80)
        vim = Controller(term, fd, pid)
        return vim
    else:  # child process runs vim
        spawn_vim(vim_command, rcfiles, files_to_edit)


def spawn_vim(vim_command='vim', rcfiles=[], files_to_edit=[]):
    import pty

    command = [vim_command, '-u']

    if rcfiles:
        command.extend(rcfiles)
    else:
        command.append('NONE')

    command.extend(files_to_edit)

    pty.spawn(command)
