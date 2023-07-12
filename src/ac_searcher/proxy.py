from random import choice

proxies = [
    'yJ98qF:LUkv6p@217.29.62.214:11792',
    'yJ98qF:LUkv6p@217.29.62.214:11791',
    'yJ98qF:LUkv6p@217.29.62.214:11790',
    'yJ98qF:LUkv6p@217.29.62.214:11789',
    'yJ98qF:LUkv6p@217.29.62.214:11788',
    'yJ98qF:LUkv6p@217.29.62.214:11787',
    'yJ98qF:LUkv6p@217.29.62.214:11786',
    'yJ98qF:LUkv6p@217.29.62.214:11785',
    'yJ98qF:LUkv6p@217.29.62.214:11784',
    'yJ98qF:LUkv6p@217.29.62.214:11783',
    'yJ98qF:LUkv6p@217.29.62.214:11782',
    'yJ98qF:LUkv6p@217.29.62.214:11781',
    'yJ98qF:LUkv6p@217.29.62.214:11780',
    'yJ98qF:LUkv6p@217.29.62.214:11779',
    'yJ98qF:LUkv6p@217.29.62.214:11778'
]

def get_random_proxy() -> dict:
    proxy = choice(proxies)
    return {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
