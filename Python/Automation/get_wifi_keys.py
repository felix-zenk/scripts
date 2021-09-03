import subprocess
import re

doprint = True
save = False


def get_available_networks():
    networks = []
    output = str(subprocess.check_output(["netsh", "wlan", "show", "networks"]))
    results = output.split('SSID ')
    for i in range(0, int(results[0].split(" Netz")[0].split("sind ")[1])):
        networks.append(results[i+1].split('\\r')[0].split(' : ')[1])
    return networks

def get_password(profile):
    out = str(subprocess.check_output(['cmd.exe', '/c netsh wlan show profile "{0}" key=clear'.format(profile)]))
    secured = out.split('Sicherheitsschl\\x81ssel')[1]
    if 'Vorhanden' in secured:
        key = out.split('Schl\\x81sselinhalt')[1].split(':')[1].split('\\r')[0].strip()
        if doprint:
            print('{0}: {1}'.format(profile, key))
        return key
    return ""

def get_saved_passwords():
    output = str(subprocess.check_output(["cmd.exe", "/c netsh wlan show profiles"]))
    profiles = [re.search(r': (.*)', profile.replace("\\r", "")).group(1) for profile in output.split("\\n") if re.search(r': (.*)', profile.replace("\r", "")) is not None]
    saved_passwords = {}
    if doprint:
        print("Saved networks:")
    for profile in profiles:
        saved_passwords[profile] = (get_password(profile))
    if save:
        file = open('wlan_info.txt', 'w')
        for profile in profiles:
            try:
                file.write('{0}: {1}\n'.format(profile, saved_passwords[profile]))
            except KeyError:
                pass
        file.close()
    return saved_passwords

def main():
    passwords = get_saved_passwords()
    available_networks = get_available_networks()
    if doprint:
        print('\nAvailable:')
    for network in passwords.keys():
        if network in available_networks and doprint:
            print(network+' : '+passwords[network])

if __name__ == '__main__':
    main()
