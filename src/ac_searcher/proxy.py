from random import choice

proxies = [
    'rLnYQF:VkEe6P@103.78.191.148:8000',
    'rLnYQF:VkEe6P@103.78.189.180:8000',
    'rLnYQF:VkEe6P@103.78.190.216:8000',
    'rLnYQF:VkEe6P@103.78.190.141:8000',
    'rLnYQF:VkEe6P@103.78.189.149:8000',
    'rLnYQF:VkEe6P@103.78.191.164:8000',
    'rLnYQF:VkEe6P@103.78.188.223:8000',
    'rLnYQF:VkEe6P@103.78.191.134:8000',
    'rLnYQF:VkEe6P@103.78.188.163:8000',
    'rLnYQF:VkEe6P@103.78.190.50:8000',
    'rLnYQF:VkEe6P@103.78.189.144:8000',
    'rLnYQF:VkEe6P@103.78.188.80:8000',
    'rLnYQF:VkEe6P@103.78.191.63:8000',
    'rLnYQF:VkEe6P@103.78.191.180:8000',
    'DbLtJx:k4S2Wc@45.154.229.84:8000',
    'DbLtJx:k4S2Wc@45.157.39.48:8000',
    'DbLtJx:k4S2Wc@45.154.229.152:8000',
    'DbLtJx:k4S2Wc@45.157.39.58:8000',
    'DbLtJx:k4S2Wc@45.118.251.238:8000',
    'DbLtJx:k4S2Wc@45.154.229.162:8000',
    'DbLtJx:k4S2Wc@45.118.251.108:8000',
    'DbLtJx:k4S2Wc@45.157.39.66:8000',
    'DbLtJx:k4S2Wc@45.154.229.221:8000',
    'DbLtJx:k4S2Wc@45.118.251.240:8000',
    'DbLtJx:k4S2Wc@45.157.39.60:8000',
    'DbLtJx:k4S2Wc@45.154.229.209:8000',
    'DbLtJx:k4S2Wc@45.118.251.95:8000',
    'DbLtJx:k4S2Wc@45.118.251.80:8000',
    'HsQQ5v:Pff8PC@45.146.129.101:8000',
    'HsQQ5v:Pff8PC@45.118.251.14:8000',
    'HsQQ5v:Pff8PC@45.157.39.148:8000',
    'HsQQ5v:Pff8PC@45.154.229.116:8000',
    'p06V6f:y2Ro1c@194.53.188.225:8000',
    'p06V6f:y2Ro1c@194.53.190.137:8000',
    'p06V6f:y2Ro1c@194.53.191.136:8000',
    'p06V6f:y2Ro1c@194.53.190.45:8000',
    'p06V6f:y2Ro1c@194.53.190.77:8000',
]

def get_random_proxy() -> dict:
    proxy = choice(proxies)
    return {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
