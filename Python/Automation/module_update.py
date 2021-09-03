def update():
    """Update every installed but outdated module
    """
    from subprocess import check_output
    from sys import executable
    from os import system
    print(' [UPDATE]: Looking for updates...')
    system(f'{executable} -m pip install --upgrade pip')
    for row in check_output([executable, "-m", "pip", "list", "--outdated"]).decode('utf-8').split('wheel\r\n')[2:-1]:
        module_info = []
        for p in row.split(' '):
            if not ' ' == p and not '' == p:
                module_info.append(p)
        print(f' [UPDATE]: Updating {module_info[0]}, v{module_info[1]} -> v{module_info[2]}')
        system(f'{executable} -m pip install --upgrade {module_info[0]}')
    print(' [UPDATE]: Everything is up to date.')

if __name__ == "__main__":
    update()
