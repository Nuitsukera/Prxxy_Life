import os
import concurrent.futures
import colorama
import time
import ctypes

# Modules
from modules.utils import faded_text
from modules.utils import computer_name
from modules.utils import user_name
from modules.functions import current_time
from modules.functions import load_config
from modules.functions import read_proxies
from modules.functions import check_proxy
from modules.functions import save_proxy
from modules.functions import output

def main():
    if os.name == "nt":
        os.system("mode con cols=120 lines=30")
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.SetWindowLongW(
                hwnd, 
                -16, 
                ctypes.windll.user32.GetWindowLongW(hwnd, -16) & ~0x00040000
            )
    
    input_folder = "input"
    config = load_config()

    if not config or ("ipstack" not in config and "ipinfo" not in config):
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Falha ao carregar a configuração. Encerrando...")
        return

    metodo = None
    access_keys = []

    if config["metodo"]["ipstack"]:
        metodo = "ipstack"
        access_keys = config["ipstack"]["access_keys"]
    elif config["metodo"]["ipinfo"]:
        metodo = "ipinfo"
        access_keys = config["ipinfo"]["access_keys"]

    if not access_keys:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Nenhuma chave de API foi encontrada para o método {metodo}.")
        return
    
    try:
        os.system('cls')
        time.sleep(1)
        print(faded_text)
        print(f"{colorama.Fore.MAGENTA} Informe o tempo limite de resposta em MS (milissegundos)")
        timeout_ms = int(input(f"{colorama.Fore.BLUE}┌──({colorama.Fore.MAGENTA}{user_name}㉿{computer_name}{colorama.Fore.BLUE})-[{colorama.Fore.WHITE}~{colorama.Fore.BLUE}]\n└─{colorama.Fore.MAGENTA}${colorama.Fore.WHITE} "))
        os.system('cls')
        print(faded_text)
        print(f"{colorama.Fore.YELLOW}[INFO]{colorama.Fore.WHITE} Tempo limite configurado: {colorama.Fore.GREEN}{timeout_ms}ms")
        
        timeout = timeout_ms / 1000
    except ValueError:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Por favor, insira um número válido.")
        return

    proxies = read_proxies(input_folder)

    if not proxies:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Nenhum proxy disponível para verificação. Encerrando...")
        return
    
    print(f"\n\n{colorama.Fore.YELLOW}[INFO]{colorama.Fore.WHITE} Iniciando a verificação de {colorama.Fore.GREEN}{len(proxies)}{colorama.Fore.WHITE} proxies...")
    time.sleep(3)
    os.system('cls')
    print(faded_text)

    all_proxies_set = set()
    found_valid_proxy = False
    proxy_types_found = set() 

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_proxy, proxy, timeout, access_keys, metodo, all_proxies_set) for proxy in proxies]

        for future in concurrent.futures.as_completed(futures):
            proxy, proxy_type, country, elapsed_time, valid = future.result()
            if valid:
                found_valid_proxy = True
                proxy_types_found.add(proxy_type)
                print(f"{current_time()} STATUS{colorama.Fore.MAGENTA}:{colorama.Fore.WHITE} {proxy} {colorama.Fore.MAGENTA}Tipo{colorama.Fore.WHITE}: {colorama.Fore.GREEN}{proxy_type}{colorama.Fore.WHITE} — {colorama.Fore.MAGENTA}País{colorama.Fore.WHITE}: {colorama.Fore.GREEN}{country}{colorama.Fore.WHITE} — {colorama.Fore.MAGENTA}Tempo de resposta{colorama.Fore.WHITE}: {colorama.Fore.GREEN}{elapsed_time:.2f}s")
                save_proxy(proxy, country, proxy_type, all_proxies_set)
                
    output(proxy_types_found)
    
    if not found_valid_proxy:
        print(f"{colorama.Fore.RED}[ERRO]{colorama.Fore.WHITE} Nenhum proxy válido encontrado.")
    else:
        print(f"{colorama.Fore.GREEN}[SUCESSO]{colorama.Fore.WHITE} Verificação concluída com sucesso!")

if __name__ == "__main__":
    main()