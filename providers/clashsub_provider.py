import yaml

from providers.provider import Provider


class ClashSubProvider(Provider):
    def fetch(self, conf) -> list:
        content = super().get_text(conf['url'])
        if content is None or len(content) == 0:
            return []
        yml = yaml.safe_load(content)
        if "proxies" not in yml or len(yml['proxies']) == 0:
            return []
        return yml['proxies']


if __name__ == '__main__':
    conf = {
        'name': 'go4sharing',
        'format': 'clash-sub',
        'url': 'https://raw.githubusercontent.com/go4sharing/sub/main/sub.yaml'
    }
    proxies = ClashSubProvider().fetch(conf)
    print(proxies)
