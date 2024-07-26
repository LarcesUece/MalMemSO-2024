import winrm
import base64

#def disable_host_network(ip):
def disable_host_network():
    ip = '192.168.0.16'

    # windows credentials
    win_user_login = "suporte"
    win_user_passwd = "123456"

    # powerShell command to disable remote network
    powershell_command = "Disable-NetAdapter -Name '*' -Confirm:$False"

    # password encryption
    #password_b64 = base64.b64encode(win_user_passwd.encode('utf-8')).decode('utf-8')

    # remote command
    conn = winrm.Session(f"http://{ip}:5985", auth=(win_user_login, win_user_passwd))
    result = conn.run_ps(powershell_command)

    # Check command status
    if result.status_code == 0:
        print("Placa de rede desabilitada com sucesso!")
        return True
    else:
        print(f"Falha ao desabilitar a placa de rede: {result.std_out}")
        return False
