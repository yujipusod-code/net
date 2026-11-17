from flask import Flask, render_template, request
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException




app = Flask(__name__)




ROUTER = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.10.74",   # netmiko uses 'host', not 'ip'
    "port": 32770,
    "username": "admin",
    "password": "eve123",
    "secret": "eve123",
    "timeout": 15,
    "session_timeout": 30,
    "global_delay_factor": 2,
}




COMMANDS = [
    "show version",
    "show ip interface brief",
    "show running-config",
]








@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None




    if request.method == "POST":
        net_connect = None
        try:
            net_connect = ConnectHandler(**ROUTER)
            net_connect.enable()




            for cmd in COMMANDS:
                # 'show running-config' is long — relax timeouts + verification
                output = net_connect.send_command(
                    cmd,
                    read_timeout=60,
                    cmd_verify=False,
                )
                results[cmd] = output




        except NetmikoAuthenticationException as e:
            error = f"Authentication failed: {e}"
        except NetmikoTimeoutException as e:
            error = f"Timed out connecting to {ROUTER['host']}:{ROUTER['port']} — {e}"
        except Exception as e:
            error = f"Unexpected error: {type(e).__name__}: {e}"
        finally:
            if net_connect is not None:
                net_connect.disconnect()




    # ALWAYS return a response — both GET and POST
    return render_template("index.html", results=results, error=error)








if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)