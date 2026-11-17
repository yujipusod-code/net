# day 3: First Netmiko connection and command execution
from netmiko import ConnectHandler


router_device = {
    'device_type' : 'cisco_ios_telnet',
    'ip': '192.168.10.74',
    'port': 32770,
    'username': 'admin',
    'password': 'eve123',
    'secret': 'eve123',
}
try:
    print("Connecting to router...")
    net_connect = ConnectHandler(**router_device)


    net_connect.enable()


    commands_to_run = [
        "show version",
        "show ip interface brief",
        "show running-config"
    ]


    for cmd in commands_to_run:
        print(f"\n--- Output for: {cmd} ---")
        output = net_connect.send_command(cmd)
        print(output)


    net_connect.disconnect()
    print("\nDisconnected successfully.")
except Exception as e:
    print(f"Connection failed: {e}")