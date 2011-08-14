import vimdriver


class vimrobot(object):

    def start_vim(self):
        self.vim = vimdriver.make(rcfiles=[], files_to_edit=[])

    def stop_vim(self):
        self.vim.stop()

    def send_keys(self, keys):
        self.vim.send_keys(keys)

    def check_until(self, global_timeout, function, args=[], kwargs={}):
        if function(*args, **kwargs):
            return True
        timeout = 0.01
        spent = 0
        while spent < global_timeout:
            if self.vim.updated(timeout) and function(*args, **kwargs):
                return True
            spent += timeout
        print 'Timeout'
        print self.vim.get_screen()
        msg = 'Timeout'
        raise AssertionError(msg)

    def _is_on_screen(self, text):
        rows = self.vim.rows
        for index, row in enumerate(rows):
            if text in row.tostring():
                return True
        return False

    def is_on_screen(self, text, timeout=0.5):
        if not self.check_until(timeout, self._is_on_screen, [text]):
            screen = self._get_screen()
            msg = '"%s" not on screen:\n\n%s' % (text, screen)
            raise AssertionError(msg)

    def _is_on_command_line(self, text):
        command_line = self.vim.rows[23].tostring()
        return text in command_line

    def is_on_command_line(self, text, timeout=0.5):
        if not self.check_until(
                timeout, self._is_on_command_line, [text]):
            command_line = self.vim.rows[23].tostring()
            msg = '"%s" not on command line:\n\n%s' % (text, command_line)
            raise AssertionError(msg)
