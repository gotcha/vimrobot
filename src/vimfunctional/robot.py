import vimdriver


class vimfunctional(object):

    def start_vim(self):
        self.vim = vimdriver.make(files_to_edit=[])

    def stop_vim(self):
        self.vim.send_keys('\x1b:q!')

    def send_keys(self, keys):
        self.vim.send_keys(keys)

    def is_on_screen(self, text):
        self.vim.update()
        rows = self.vim.rows
        for row in rows:
            print row.tostring()
            if text in row.tostring():
                return
        screen = '\n'.join([row.tostring() for row in rows])
        msg = '%s not on screen.\n\n%s' % (text, screen)
        raise AssertionError(msg)

    def is_on_command_line(self, text):
        self.vim.update()
        command_line = self.vim.rows[23].tostring()
        if text not in command_line:
            msg = '%s not on command line.\n\n%s' % (text, command_line)
            raise AssertionError(msg)
