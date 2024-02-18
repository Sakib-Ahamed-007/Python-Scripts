import subprocess
import optparse
import re


def parse_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface of the NIC")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Interface not provided!")
    elif not options.new_mac:
        parser.error("MAC address not provided!")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address of " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# gets the current MAC address from the ifconfig result
def get_mac(interface):
    # REGEX to match mac address
    mac_address_regex = r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})"
    encoding = 'utf-8'
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode(encoding)
    found_mac = re.search(mac_address_regex, ifconfig_result)
    if found_mac:
        return found_mac.group(0)


options = parse_arguments()
mac_address_before_change = get_mac(options.interface) 
print(f"[+] Current MAC address {mac_address_before_change}")
change_mac(options.interface, options.new_mac) 
mac_address_after_change = get_mac(options.interface)

if mac_address_after_change:
    if((mac_address_before_change != mac_address_after_change)):
        print(f"[+] MAC address changed successfully to {mac_address_after_change}")
    else:
        print("[-] You entered the old MAC address!!")
else:
    print("[-] Could not change the MAC address!")
    
