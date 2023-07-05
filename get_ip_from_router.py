#!/usr/bin/python3
from netmiko import ConnectHandler
import configparser
import json

config = configparser.ConfigParser()

# INIファイルを読み込み
config.read('config.ini')

for section in config.sections():
    # デバイスの接続情報を設定
    print(section + ": ")
    device = {
        'device_type': config.get(section, "device_type"),
        'ip': config.get(section, "ip_address"),
        'port': int(config.get(section, "port")),  # Telnetポート番号
    }

    # デバイスにtelnet接続
    telnet_connection = ConnectHandler(**device)
    prompt = telnet_connection.find_prompt()
    print(f"接続成功: {prompt}")

    if config.get(section, "device_type") == "cisco_ios_telnet":
        output = telnet_connection.send_command('show ip interface brief')

        # 出力結果からIPアドレスとインタフェース情報を抽出
        lines = output.splitlines()[2:5]  # ヘッダーと最終行を除外
        interfaces = []
        for line in lines:
            interface, ip_address, _, method, status, protocol = line.split()[:6]
            interfaces.append({
                "interface": interface,
                "ipaddress": ip_address,
                "method" : method,
                "status": status,
                "protocol": protocol,
                })

        # 結果を表示
        print("インタフェース情報:")
        for interface in interfaces:
            interface_json_data = json.dumps(interface)

            # JSON文字列の表示
            print(interface_json_data)

    # Telnet接続を閉じる
    telnet_connection.disconnect()

