# Prxxy Life ~ Checker

Faça a checagem e organização de proxies HTTP, SOCKS4 e SOCKS5.

- Pode determinar se o proxy é anônimo.
- Suporta a determinação da geolocalização do nó de saída do proxy.
- Pode classificar proxies por velocidade.
- Oferece suporte a proxies com autenticação.

## Instalação e uso

### Executável

Para fazer a instalação de todas as dependências e criar as pastas necessárias, apenas execute o arquivo  [setup.bat](setup.bat)., não é necessário executar como administrador.

### Uso

Após a instalação ser concluída será criada uma pasta chamada "input" nessa pasta você irá colocar seus arquivos de texto contendo os proxies, gostaria de lembrar de que os arquivos devem ser unicamente .txt e os proxies devem estar nos seguintes formatos abaixo

  ```
  # IP:PORT
  85.214.107.177:80
  18.223.25.15:80
  203.115.101.55:82
  203.115.101.61:82
  50.174.7.159:80
  50.207.199.87:80
  32.223.6.94:80
  82.119.96.254:80
  13.38.153.36:80
  13.37.89.201:80

  # IP:PORT:USERNAME:PASSWORD
  198.23.239.134:6540:nuitsukera:ex3ps3q2fdfz
  207.244.217.165:6712:nuitsukera:ex3ps3q2fdfz
  107.172.163.27:6543:nuitsukera:ex3ps3q2fdfz
  64.137.42.112:5157:nuitsukera:ex3ps3q2fdfz
  173.211.0.148:6641:nuitsukera:ex3ps3q2fdfz
  161.123.152.115:6360:nuitsukera:ex3ps3q2fdfz
  23.94.138.75:6349:nuitsukera:ex3ps3q2fdfz
  154.36.110.199:6853:nuitsukera:ex3ps3q2fdfz
  173.0.9.70:5653:nuitsukera:ex3ps3q2fdfz
  173.0.9.209:5792:nuitsukera:ex3ps3q2fdfz
  ```

### Execução

#### Terminal

Após todo esse processo, abra o terminal ou cmd no diretório raiz e execute o seguinte comando abaixo

```
python main.py
```
Após o programa iniciar você apenas irá inserir o tempo de resposta máximo para cada proxy, os proxies que respeitarem o tempo limite serão salvos na pasta output, vamos seguir abaixo um mapa dos possíveis arquivos que podem ser criados dentro da pasta output

```
- all country/
  - all proxies/
    - proxies.txt  
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt

- br/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- us/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- cn/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- de/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- fr/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- gb/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- jp/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- in/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- it/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- ca/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- au/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- ru/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- mx/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- kr/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- sa/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
- za/
  - http/
    - proxies.txt
  - socks4/
    - proxies.txt
  - socks5/
    - proxies.txt
```
