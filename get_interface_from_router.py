#!/usr/bin/python3
from netmiko import ConnectHandler
import configparser
import json

config = configparser.ConfigParser()

# INIファイルを読み込み
config.read('config.ini')

for section in config.sections():
    # デバイスの接続情報を設定
    device = {
        'device_type': config.get(section, "device_type"),
        'username': config.get(section, "user"),
        'ip': config.get(section, "ip_address"),
        'port': int(config.get(section, "port")),  # Telnetポート番号
    }

    # デバイスにtelnet接続
    telnet_connection = ConnectHandler(**device)
    prompt = telnet_connection.find_prompt()

    if config.get(section, "device_type") == "cisco_ios_telnet":
        output = telnet_connection.send_command('show ip interface brief')

        # 出力結果からIPアドレスとインタフェース情報を抽出
        lines = output.splitlines()[2:]  # ヘッダーを除外
        interfaces = []
        for line in lines:
            if len(line.split()) == 6:
                interface, ip_address, _, method, status, protocol = line.split()[:6]
                interfaces.append({
                    "interface": interface,
                    "ipaddress": ip_address,
                    "method" : method,
                    "status": status,
                    "protocol": protocol,
                    })

    if config.get(section, "device_type") == "arista_eos_telnet":
        output = telnet_connection.send_command('show ip interface brief')

        # 出力結果からIPアドレスとインタフェース情報を抽出
        lines = output.splitlines()[3:]  # ヘッダーを除外
        interfaces = []
        for line in lines:
            if len(line.split()) == 5:
                interface, ip_address, status, protocol, mtu = line.split()[:5]
                interfaces.append({
                    "interface": interface,
                    "ipaddress": ip_address,
                    "status": status,
                    "protocol": protocol,
                    "mtu": mtu,
                    })

    # 結果を表示
    print(json.dumps({section: interfaces}))

    # Telnet接続を閉じる
    telnet_connection.disconnect()

