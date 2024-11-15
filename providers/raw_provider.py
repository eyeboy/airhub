import base64
import json

from log import get_logger
from providers.provider import Provider


# https://lsz3034.github.io/clash-yml/qrcode/2.html

def vmess2clash(vmess_url: str):
    # 提取 Base64 部分
    base64_str = vmess_url[8:]
    # 替换 URL 特殊字符
    base64_str = base64_str.replace('-', '+').replace('_', '/')
    # 处理 padding
    while len(base64_str) % 4 != 0:
        base64_str += '='
    # Base64 解码。注意：在 Python3 中 b64decode 返回 bytes 类型，需要解码成 string。
    decoded_json = base64.b64decode(base64_str).decode('utf-8')
    # 解析 JSON
    config = json.loads(decoded_json)
    return {
        "name": config.get("ps", "Unnamed"),
        "type": "vmess",
        "server": config.get("add", "example.com"),
        "port": config.get("port", 443),
        "uuid": config.get("id", ""),
        "alterId": config.get("aid", 0),
        "cipher": "auto",
        "tls": config.get("tls") is not None and config.get("tls").lower() != 'none',
        "skip-cert-verify": True,
        "network": config.get("net", "ws"),
        "ws-opts": {
            "path": config.get("path", "/"),
            "headers": {
                "Host": config.get('host', config.get('add', config.get('example.com')))
            }
        }
    }


class RawProvider(Provider):
    def fetch(self, conf) -> list:
        logger = get_logger()
        content = super().get_text(conf['url'])
        urls = content.split('\n')
        proto_urls = set(urls)
        clash_proxies = []
        for url in proto_urls:
            if len(url) == 0:
                continue
            if not url.startswith('vmess'):
                logger.warning('unsupported protocol: %s', url)
            clash_proxies.append(vmess2clash(url))
        return clash_proxies


if __name__ == '__main__':
    provider = RawProvider()
    provider.fetch(conf={
        'name': 'vpn.fail-v2ray',
        'format': 'raw',
        'url': 'https://vpn.fail/free-proxy/v2ray'
    })

