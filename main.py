import g4f, asyncio, sys, time
import os, platform
import json
import random
import requests
import datetime

global conf_file
global config

global broken
global req_auth
global req_chromedriver

broken = ["Yqcloud", "Llama2", "Hashnode", "GptTalkRu", "GptForLove", 
                "GPTalk", "Chatxyz", "ChatgptNext", "Chatgpt4Online", "ChatForAi", 'DeepInfra', 'HuggingChat', 'GptChatly']

req_auth = ["Bard", "ThebApi", "Raycast", "Poe", "OpenaiChat"]

req_chromedriver = ["Theb", "TalkAi", "Pi", "PerplexityAi", "MyShell", "AItianhuSpace"]

if platform.system() == 'Linux':
    conf_dir = os.path.join(os.path.expanduser('~'), '.config/gpt4cli/')
    conf_file = os.path.join(conf_dir, 'gpt4cli.json')
    conv_dir = os.path.join(os.path.expanduser('~'), '.config/gpt4cli/conversations')


def retrieve_cookies(website):
    for prefix in ['http://', 'https://']:
        url = prefix + website
        try:
            response = requests.get(url)
            response.raise_for_status()
                 
            if response.cookies:
                print('\033[92mSuccessfully retrieved cookies.\033[0m')
                return response.cookies.get_dict()
            else:
                print('\033[91mNo cookies detected.\033[0m')
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


def color_providers(providers):

    global broken
    global req_auth
    global req_chromedriver

    for i in range(len(providers)):
        if providers[i] in req_auth:
            providers[i] = f"\033[93m{providers[i]}\033[0m"
        elif providers[i] in req_chromedriver:
            providers[i] = f"\033[95m{providers[i]}\033[0m"
        elif providers[i] in ['You', 'Aura', 'Phind', 'FakeGpt']:
            providers[i] = f"\033[92m{providers[i]}\033[0m"

    return providers

def check_providers():

    global broken

    gpt35_providers = []
    gpt4_providers = []
    nongpt_providers = []
    gpt3_providers = []
    other_providers = []

    for provider in g4f.Provider.__providers__:
        if provider.working:
            if provider.__name__ in broken:
                continue
            if provider.__name__ in ['Bing', 'GptChatly', 'Liaobots', 'Phind', 'Aura']:
                gpt4_providers.append(provider.__name__)
            elif provider.__name__ in ['Bard', 'DeepInfra', 'HuggingChat', 'Llama2', 'OpenAssistant', 'Pi']:
                nongpt_providers.append(provider.__name__)
            elif provider.__name__ in ['Koala', 'Gpt6', 'ChatgptAi', 'OnlineGpt', 'ChatgptDemo', 'You', 'GptGo', 'TalkAi']:
                gpt3_providers.append(provider.__name__)
            elif provider.__name__ in ['Raycast', 'Poe', 'Theb', 'ThebApi', 'PerplexityAi', 'AItianhuSpace', 'MyShell']:
                other_providers.append(provider.__name__)
            else:
                gpt35_providers.append(provider.__name__)

    return gpt35_providers, gpt4_providers, nongpt_providers, gpt3_providers, other_providers

def edit_config():

    global broken
    global req_auth
    global req_chromedriver

    dtpret = 0
    dtp = None


    while True:
        if dtpret == 0:
            dtp = input('Do you wanna default to some provider? (y/n): ')
        else:
            dtp = input(f'{dtp} is neither y or n silly. Do you wanna default to some provider? (y/n): ')
        
        if dtp.lower() in ['y', 'n']:
            break
            
        dtpret += 1


    if dtp.lower() == 'y':

        gpt35_providers, gpt4_providers, nongpt_providers, gpt3_providers, other_providers = check_providers()
        
        providers = gpt35_providers + gpt4_providers + other_providers + gpt3_providers + nongpt_providers

        gpt35_providers = color_providers(gpt35_providers)
        gpt3_providers = color_providers(gpt3_providers)
        gpt4_providers = color_providers(gpt4_providers)
        nongpt_providers = color_providers(nongpt_providers)
        other_providers = color_providers(other_providers)

        print("\033[93mYellow - Requires authorization. Everything except Bard can't be authorized at the moment as i have no way of testing. (OpenAI  didn't work for me, you can try)\033[0m\n")
        print("\033[95mPurple - Requires chromedriver.\033[0m\n")
        print('\033[92mGreen - Recommended\033[0m\n')

        print(f'\nGPT 4 Providers: {", ".join(gpt4_providers)}')
        print(f'GPT 3.5 Providers: {", ".join(gpt35_providers)}')
        print(f'GPT 3 Providers: {", ".join(gpt3_providers)}')
        print(f'Non OpenAI Providers: {", ".join(nongpt_providers)}')
        print(f'Other Providers (could not test, multimodel etc.): {", ".join(other_providers)}\n')
        
        dp = input("To which provider do you want to default to? (Make sure to use proper capitalization): ")

    #ci = input('Insert your custom instructions. The chatbot will be told this alongside your prompt (Leave empty if you dont want to use this): ')

    lcret = 0

    while True:
        if lcret == 0:
            lc = input('Do you want to log conversations? (y/n): ')
        else:
            lc = input(f'{dtp} is neither y or n silly. Do you want to log conversations? (y/n): ')
        
        if lc.lower() in ['y', 'n']:
            break

        lcret +=1

    config = {
        'default_provider': None if dtp.lower() == 'n' else dp,
        'log_convos': True if lc.lower() == 'y' else False
    }

    with open(conf_file, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    global config
    global conf_file
    global conv_dir
    with open(conf_file, 'r') as f:
        config = json.load(f)
    
    if config['log_convos'] is True:
        os.makedirs(conv_dir, exist_ok=True)


def main():
    global config

    os.makedirs(conf_dir, exist_ok=True)

    ascii_arts = ['''
    \u001b[38;2;255;0;0m _____ ______ _____ ___ _____  _     _____ \u001b[0m
    \u001b[38;2;255;165;0m|  __ \| ___ \_   _/   /  __ \| |   |_   _|\u001b[0m
    \u001b[38;2;255;255;0m| |  \/| |_/ / | |/ /| | /  \/| |     | |  \u001b[0m
    \u001b[38;2;0;128;0m| | __ |  __/  | / /_| | |    | |     | |  \u001b[0m
    \u001b[38;2;0;0;255m| |_\ \| |     | \___  | \__/\| |_____| |_ \u001b[0m
    \u001b[38;2;128;0;128m \____/\_|     \_/   |_/\____/\_____/\___/\u001b[0m
    ''',
    """
    \033[38;5;39m _____ ______ _____ ___ _____  _     _____ \033[0m
    \033[38;5;218m|  __ \| ___ \_   _/   /  __ \| |   |_   _|\033[0m
    \033[38;5;15m| |  \/| |_/ / | |/ /| | /  \/| |     | |  \033[0m
    \033[38;5;15m| | __ |  __/  | / /_| | |    | |     | |  \033[0m
    \033[38;5;218m| |_\ \| |     | \___  | \__/\| |_____| |_ \033[0m
    \033[38;5;39m \____/\_|     \_/   |_/\____/\_____/\___/\033[0m
    """,
    '''
    \033[38;5;220m _____ ______ _____ ___ _____  _     _____ \033[0m
    \033[38;5;208m|  __ \| ___ \_   _/   /  __ \| |   |_   _|\033[0m
    \033[38;5;196m| |  \/| |_/ / | |/ /| | /  \/| |     | |  \033[0m
    \033[38;5;198m| | __ |  __/  | / /_| | |    | |     | |  \033[0m
    \033[38;5;206m| |_\ \| |     | \___  | \__/\| |_____| |_ \033[0m
    \033[38;5;51m \____/\_|     \_/   |_/\____/\_____/\___/\033[0m
    ''',
    '''
    \033[38;5;39m _____ ______ _____ ___ _____  _     _____ \033[0m
    \033[38;5;38m|  __ \| ___ \_   _/   /  __ \| |   |_   _|\033[0m
    \033[38;5;37m| |  \/| |_/ / | |/ /| | /  \/| |     | |  \033[0m
    \033[38;5;36m| | __ |  __/  | / /_| | |    | |     | |  \033[0m
    \033[38;5;35m| |_\ \| |     | \___  | \__/\| |_____| |_ \033[0m
    \033[38;5;34m \____/\_|     \_/   |_/\____/\_____/\___/\033[0m
    ''',
    '''
    \033[38;5;218m _____ ______ _____ ___ _____  _     _____ \033[0m
    \033[38;5;218m|  __ \| ___ \_   _/   /  __ \| |   |_   _|\033[0m
    \033[38;5;218m| |  \/| |_/ / | |/ /| | /  \/| |     | |  \033[0m
    \033[38;5;218m| | __ |  __/  | / /_| | |    | |     | |  \033[0m
    \033[38;5;218m| |_\ \| |     | \___  | \__/\| |_____| |_ \033[0m
    \033[38;5;218m \____/\_|     \_/   |_/\____/\_____/\___/\033[0m
    '''
    ]

    print("\n\n\n")
    print(random.choice(ascii_arts))
    print("\n\n\n")

    if not os.path.exists(conf_file):
        edit_config()
    
    load_config()
    print('Type "EDIT CONFIG" in any text prompt to edit your config\nType "EXIT" in any text prompt to exit (or just Ctrl C)')

    provider = None

    if config['default_provider'] is None:

        gpt35_providers, gpt4_providers, nongpt_providers, gpt3_providers, other_providers = check_providers()
        providers =  gpt35_providers + gpt4_providers + other_providers + gpt3_providers + nongpt_providers

        gpt35_providers = color_providers(gpt35_providers)
        gpt3_providers = color_providers(gpt3_providers)
        gpt4_providers = color_providers(gpt4_providers)
        nongpt_providers = color_providers(nongpt_providers)
        other_providers = color_providers(other_providers)

        print("\n\033[93mYellow - Requires authorization. Everything except Bard can't be authorized at the moment as i have no way of testing. (OpenAI  didn't work for me, you can try)\033[0m")
        print("\033[95mPurple - Requires chromedriver.\033[0m")
        print('\033[92mGreen - Recommended\033[0m')

        print(f'\nGPT 4 Providers: {", ".join(gpt4_providers)}')
        print(f'GPT 3.5 Providers: {", ".join(gpt35_providers)}')
        print(f'GPT 3 Providers: {", ".join(gpt3_providers)}')
        print(f'Non OpenAI Providers: {", ".join(nongpt_providers)}')
        print(f'Other Providers (could not test, multimodel etc.): {", ".join(other_providers)}\n')

        while True:
            provider = input('Choose your provider: ')

            if provider == 'EDIT CONFIG':
                edit_config()
                print('Restart required.')
                exit()
            elif provider == 'EXIT':
                print('\n\nExiting...')
                exit()
            elif provider not in providers:
                print('Invalid provider. Make sure to capitalize properly.')
            else:
                break
        
    else:
        provider = config['default_provider']

    cookies = {}

    if provider == 'Liaobots':
        print('\033[93mLiaobots is protected by cloudflare. It may not work!\033[0m')

    elif provider == 'Bard':
        print('\033[93mBard requires authentication! Attempting to retrieve cookies...\033[0m')
        cookies = retrieve_cookies('google.com')

    elif provider == 'OpenaiChat':
        print('\033[93mOpenAI requires authentication! Attempting to retrieve cookies...\033[0m')
        cookies = retrieve_cookies('openai.com')
    
    elif provider == 'Bing':
         print('\033[93mBing is very slow. Use Aura instead.\033[0m')
    


    for prov in g4f.Provider.__providers__:
        if prov.working:
            if prov.__name__ == provider.capitalize():
                provider = prov
                break
    
    past_prompts = []
    past_replies = []
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    while True:

        try:
            past = ""

            if past_prompts:
                past += "CONTINUE THIS CONVERSATION\n"
                for i in range(0, len(past_prompts)):
                    past += f"Previous user prompt #{i}: {past_prompts[i]}\n{past_replies[i]}\n"

            prompt = input('\nPrompt: ')

            if prompt == 'EDIT CONFIG':
                edit_config()
                print('Restart required.')
                exit()
            elif prompt == 'EXIT':
                print('\n\nExiting...')
                exit()

            response = g4f.ChatCompletion.create(
                provider = provider,
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": past + prompt}],
                auth = cookies
            )

            past_prompts.append(prompt)
            past_replies.append(response)

            print(f"\nAI: {response}")

            with open(os.path.join(conv_dir, f'{provider.__name__}_{date}'), 'a') as f:
                f.write(f'Prompt: {prompt}\n')
                f.write(f'AI: {response}\n')

        except KeyboardInterrupt:
            print('\n\nKeyboard Interrupt. Exiting...')
            exit()

        except Exception as e:
            print(e)
        
        

if __name__ == "__main__":
    main()