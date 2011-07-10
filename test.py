import vimdriver


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
    vim = vimdriver.make(files_to_edit=['afile.py'])
    print_status(vim)
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
