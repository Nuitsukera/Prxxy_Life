import os
import colorama
import requests
import timeit
import yaml
from datetime import datetime
from typing import Tuple, Optional

def current_time() -> str:
    """Retorna a hora atual formatada como [hh:mm:ss]."""
    return datetime.now().strftime(f"{colorama.Fore.MAGENTA}[{colorama.Fore.WHITE} %H:%M:%S {colorama.Fore.MAGENTA}]{colorama.Fore.WHITE}")

def load_config() -> dict:
    """Carrega o arquivo de configuração com as chaves de API e valida a configuração."""
    try:
        with open("config.yml", "r") as file:
            config = yaml.safe_load(file)
            
            if config["metodo"]["ipstack"] and config["metodo"]["ipinfo"]:
                print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Ambos os métodos ipstack e ipinfo estão ativados. Apenas um deve ser habilitado.")
                return {}
            if not config["metodo"]["ipstack"] and not config["metodo"]["ipinfo"]:
                print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Nenhum dos métodos ipstack ou ipinfo está ativado. Pelo menos um deve ser habilitado.")
                return {}
            
            return config
    except FileNotFoundError:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} O arquivo config.yml não foi encontrado.")
        return {}
    except yaml.YAMLError as e:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Erro ao carregar o arquivo config.yml: {e}")
        return {}

def read_proxies(input_folder: str) -> list:
    """Lê os proxies dos arquivos na pasta de entrada, considerando credenciais de autenticação."""
    proxies = []
    if not os.path.exists(input_folder):
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} A pasta ({input_folder}) não foi encontrada.")
        return proxies

    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                file_proxies = file.read().splitlines()
                proxies.extend(file_proxies)

    if not proxies:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Nenhum proxy foi encontrado.")
    else:
        print(f"{colorama.Fore.YELLOW}[INFO]{colorama.Fore.WHITE} Total de proxies carregados: {colorama.Fore.GREEN}{len(proxies)}")
    return proxies

def check_proxy(proxy: str, timeout: int, access_keys: list, metodo: str, all_proxies_set: set) -> Tuple[str, str, str, float, bool]:
    """Verifica se o proxy é válido e retorna informações."""
    start_time = timeit.default_timer()
    
    ip, port, username, password = parse_proxy(proxy)
    proxy_url = f"http://{username}:{password}@{ip}:{port}" if username and password else f"http://{ip}:{port}"
    proxy_type = detect_proxy_type(proxy)
    
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_type in ["http", "anonymous"] else {proxy_type: proxy_url}
    
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout)
        elapsed_time = timeit.default_timer() - start_time
        
        if elapsed_time > timeout:
            print(f"{current_time()} STATUS{colorama.Fore.MAGENTA}:{colorama.Fore.WHITE} {proxy}{colorama.Fore.RED} Inválido {colorama.Fore.WHITE}—{colorama.Fore.YELLOW} Excedeu o tempo limite.")
            return proxy, proxy_type, "unknown", elapsed_time, False
        
        if response.status_code == 200:
            country = get_country(proxy, access_keys, metodo)
            print(f"{current_time()} STATUS{colorama.Fore.MAGENTA}:{colorama.Fore.WHITE} {proxy} {colorama.Fore.MAGENTA}Tipo{colorama.Fore.WHITE}: {colorama.Fore.GREEN}{proxy_type}{colorama.Fore.WHITE} — {colorama.Fore.MAGENTA}País{colorama.Fore.WHITE}: {colorama.Fore.GREEN}{country}{colorama.Fore.WHITE} — {colorama.Fore.MAGENTA}Tempo de resposta{colorama.Fore.WHITE}: {colorama.Fore.GREEN}{elapsed_time:.2f}s")
            return proxy, proxy_type, country, elapsed_time, True
    except requests.RequestException:
        elapsed_time = timeit.default_timer() - start_time
        print(f"{current_time()} STATUS{colorama.Fore.MAGENTA}: {colorama.Fore.WHITE}{proxy}{colorama.Fore.RED} Inválido")
        
    return proxy, proxy_type, "unknown", float("inf"), False

def parse_proxy(proxy: str) -> Tuple[str, str, str, str]:
    """Parseia o proxy no formato ip:port:username:password e retorna as partes."""
    try:
        ip, port, username, password = proxy.split(":")
        return ip, port, username, password
    except ValueError:
        return proxy, None, None, None

def detect_proxy_type(proxy: str) -> str:
    """Detecta o tipo de proxy (HTTP, SOCKS4, SOCKS5 ou anônimo)."""
    if proxy.startswith("socks5"):
        return "socks5"
    elif proxy.startswith("socks4"):
        return "socks4"
    elif is_anonymous_proxy(proxy):
        return "anonymous"
    return "http"

def is_anonymous_proxy(proxy: str) -> bool:
    """Verifica se o proxy é anônimo."""
    try:
        proxies = {"http": proxy, "https": proxy}
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if response.status_code == 200:
            original_ip = requests.get("http://httpbin.org/ip").json()["origin"]
            proxy_ip = response.json()["origin"]
            return original_ip != proxy_ip
    except requests.RequestException:
        pass
    return False

def get_country(proxy: str, access_keys: list, metodo: str) -> Optional[str]:
    """Obtém o país de origem do proxy usando a API configurada (ipstack ou ipinfo)."""
    ip, _, _, _ = parse_proxy(proxy)
    try:
        if metodo == "ipstack":
            access_key = access_keys[0]
            url = f"http://api.ipstack.com/{ip}?access_key={access_key}"
        elif metodo == "ipinfo":
            access_key = access_keys[0]
            url = f"http://ipinfo.io/{ip}/country?token={access_key}"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            country = response.text.strip()
            return country.lower()
    except requests.RequestException as e:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Falha ao detectar o país do proxy {proxy}: {e}")
    return "unknown"

def output(proxy_types_found):
    """Cria as pastas principais de saída, se necessário."""
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/all country", exist_ok=True)
    os.makedirs("output/all country/http", exist_ok=True)
    os.makedirs("output/all country/all proxies", exist_ok=True)
    
    if "socks4" in proxy_types_found:
        os.makedirs("output/all country/socks4", exist_ok=True)
    if "socks5" in proxy_types_found:
        os.makedirs("output/all country/socks5", exist_ok=True)

def save_proxy(proxy: str, country: str, proxy_type: str, all_proxies_set: set):
    """Salva o proxy em arquivos específicos de acordo com o país e tipo, além de um arquivo global, evitando duplicações."""

    if proxy in all_proxies_set:
        return 
    all_proxies_set.add(proxy)

    all_proxies_path = os.path.join("output", "all country", "all proxies")
    os.makedirs(all_proxies_path, exist_ok=True)
    
    all_proxies_file_path = os.path.join(all_proxies_path, "proxies.txt")
    if os.path.exists(all_proxies_file_path):
        with open(all_proxies_file_path, "r") as file:
            existing_proxies = file.read().splitlines()
            if proxy in existing_proxies:
                return
    
    with open(all_proxies_file_path, "a") as file:
        file.write(proxy + "\n")

    folder_all_country_path = os.path.join("output", "all country", proxy_type)
    os.makedirs(folder_all_country_path, exist_ok=True)
    all_country_file_path = os.path.join(folder_all_country_path, "proxies.txt")
    if os.path.exists(all_country_file_path):
        with open(all_country_file_path, "r") as file:
            existing_proxies = file.read().splitlines()
            if proxy in existing_proxies:
                return
    
    with open(all_country_file_path, "a") as file:
        file.write(proxy + "\n")

    folder_country_path = os.path.join("output", country, proxy_type)
    os.makedirs(folder_country_path, exist_ok=True)
    country_file_path = os.path.join(folder_country_path, "proxies.txt")
    if os.path.exists(country_file_path):
        with open(country_file_path, "r") as file:
            existing_proxies = file.read().splitlines()
            if proxy in existing_proxies:
                return
    
    with open(country_file_path, "a") as file:
        file.write(proxy + "\n")
