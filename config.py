import profile

import json, os.path, typing

CONFIG_TEMPLATE = {
    'token' : 'YOUR_TOKEN_HERE',
    'channel' : [0],
    'profiles' : {
        'hello' : {
            'command' : ['echo', 'Hello world!'],
            'console' : False
        }
    }
}

config = {}

def load_config() -> bool:
    global config

    if not os.path.exists('config.json'):
        with open('config.json', 'w') as config_file:
            config_file.write(json.dumps(CONFIG_TEMPLATE))

        return False

    with open('config.json', 'r') as config_file:
        tmp_config = json.loads(config_file.read())
        
        config['token'] = tmp_config['token']
        config['channel'] = tmp_config['channel']

        config['profiles'] = {}
        for key in tmp_config['profiles']:
            config['profiles'][key] = profile.Profile(
                tmp_config['profiles'][key]['command'],
                tmp_config['profiles'][key]['console'],
                tmp_config['profiles'][key].get('directory')
            )

    return True

def get_token() -> str:
    return config['token']

def get_channels() -> typing.List[int]:
    return config['channel']

def get_profile(key: str) -> typing.Optional[profile.Profile]:
    return config['profiles'].get(key)