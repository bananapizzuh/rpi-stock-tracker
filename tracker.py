import feedparser, smtplib, os, sys, toml
from datetime import datetime
from time import mktime

config = {}
vendors = ['semaf', 'seeedstudio', 'rasppishop', 'pishopch', 'pishopca', 'piaustralia', 'mchobby', 'berrybase', 'welectron', 'tiendatec', 'reichelt', 'rasppishop', 'pi3g', 'melopero', 'kubii', '330ohms', 'raspberrystore', 'okdonl', 'mauserpt', 'farnell', 'elektronica', 'electrokit', 'coolcomp', 'botland', 'thepihut', 'rapid', 'pimoroni', 'okdouk', 'newark', 'digikeyus', 'chicagodist', 'adafruit', 'sparkfun', 'pishopza', 'pishopus', 'okdous']
countries = ['ZA', 'PT', 'PL', 'NL', 'MX', 'IT', 'FR', 'DE', 'CN', 'CA', 'BE', 'AU', 'AT', 'ES', 'SE', 'CH', 'UK', 'US']
categories = ['PIZERO', 'PI4', 'PI3', 'CM4', 'CM3']

def generate_config():
    toml_string = """
    [gmail]
    recipent = ""
    username = ""
    password = ""
    
    [parameters]
    vendors = []
    country = ""
    categories = []"""

    parsed_toml = toml.loads(toml_string)
    new_toml_string = toml.dumps(parsed_toml)

    if not os.path.isfile("./config.toml"):
        with open('config.toml', 'w') as f:
            new_toml_string = toml.dump(parsed_toml, f)

def get_config():
    return toml.load('./config.toml')

def build_params():
    vendor_params = 'vendor='
    country_params = 'country='
    category_params = 'cat='

    if config['parameters']['country'] == None:
        for vendor in config['parameters']['vendors']:
            if vendor not in vendors:
                print(f'Invalid vendor: {vendor}')
            else:
                vendor_params += vendor + '&2C'
    for category in config['parameters']['categories']:
        if category not in categories:
            print(f'Invalid category: {category}')
        else:
            category_params += category + '&2C'

    if config['parameters']['country'] not in countries and config['parameters']['vendors'] == []:
        print(f"Invalid country: {config['parameters']['country']}")
    else:
        country_params += config['parameters']['country']
    
    return '?' + vendor_params + '&' + country_params + '&' + category_params

def send_email(msg, to_addr, from_addr, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg)
    server.quit()

def parse_rss(parameters):
    url = f'https://rpilocator.com/feed/?{parameters}' #f'https://rpilocator.com/feed/?{parameters}'
    feed = feedparser.parse(url)
    if feed['entries'] != []:
        modified_cache = read_modified()
        if modified_cache != None:
            if datetime.strptime(modified_cache, '%Y-%m-%d %H:%M:%S') < datetime.fromtimestamp(mktime(feed['entries'][0]['published_parsed'])):
                send_email(feed['entries'][0]['summary'], config['gmail']['recipent'], config['gmail']['username'], config['gmail']['password'])
        else:
            export_modified(datetime.fromtimestamp(mktime(feed['entries'][0]['published_parsed'])))
        
    else:
        export_modified("")

def read_modified():
    if os.path.isfile('./modified.txt'):
        with open('./modified.txt', 'r') as file:
            return file.readline().strip()

def export_modified(input):
    with open('./modified.txt', 'w') as file:
        file.write(str(input))

def main():
    global config
    generate_config()
    config = get_config()
    parse_rss(build_params())

main()