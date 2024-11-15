import os.path

import yaml

from providers.clashsub_provider import ClashSubProvider
from providers.raw_provider import RawProvider


def uniq_proxies(proxies: list) -> list:
    uniq_proxy_set = set()
    proxy_base_name_d = dict()
    uniq_proxy_name_set = set()
    all_proxies = []
    for p in proxies:
        key = f'{p["server"]}#{p["port"]}'
        if key in uniq_proxy_set:
            continue
        uniq_proxy_set.add(key)

        proxy_name = p['name']
        if proxy_name in proxy_base_name_d:
            new_proxy_name = f'{proxy_name}_{proxy_base_name_d[proxy_name]}'
            proxy_base_name_d[proxy_name] = proxy_base_name_d[proxy_name] + 1
            while new_proxy_name in uniq_proxy_name_set:
                new_proxy_name = f'{proxy_name}_{proxy_base_name_d[proxy_name]}'
                proxy_base_name_d[proxy_name] = proxy_base_name_d[proxy_name] + 1
            proxy_name = new_proxy_name
        else:
            proxy_base_name_d[proxy_name] = 1

        uniq_proxy_name_set.add(proxy_name)
        p['name'] = proxy_name
        all_proxies.append(p)
    return all_proxies


def save_proxies(proxies, filename):
    if len(proxies) == 0:
        return
    all_proxies = []
    data = {'proxies': []}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            origin_proxies = data.get('proxies', [])
            if origin_proxies is not None and len(origin_proxies) > 0:
                all_proxies.extend(origin_proxies)
    all_proxies.extend(proxies)
    u_proxies = uniq_proxies(all_proxies)
    data['proxies'] = u_proxies
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)


with open('providers.yml', 'r') as f:
    data = yaml.safe_load(f)
    providers = data.get('providers', [])
    proxies = []
    for provider_conf in providers:
        provider_type = provider_conf['type']
        if provider_type == 'raw':
            ps = RawProvider().fetch(provider_conf)
            if len(ps) > 0:
                proxies.extend(ps)
        elif provider_type == 'clash-sub':
            proxies.extend(ClashSubProvider().fetch(provider_conf))
    save_proxies(proxies, 'source-proxies.yml')
