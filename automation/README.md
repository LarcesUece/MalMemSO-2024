

# Extração de Dumps de Memória

### Detalhes da Máquina Virtual
- **Sistema Operacional:** Windows 10
- **Memória RAM:** 2GB
- **Armazenamento:** 80GB

### Ferramentas Utilizadas
-  [Dumpit For Windows](https://www.magnetforensics.com/resources/magnet-dumpit-for-windows/)

    > *MAGNET DumpIt for Windows (created by Comae Technologies and acquired by Magnet Forensics in 2022) generates full memory crash dumps that are interoperable with multiple analysis tools and products such as WinDbg, Comae Platform.*

- [python3](https://www.python.org/downloads/windows/)

### Procedimento de Extração

É utilizado o código em python `dump-extractor.py` para automatizar a extração dos dumps de memória. Os dumps vão ser criados a cada 1 minuto, pelo tempo que for especificado pelo usuário no código.

Na Máquina Virtual do Windows, é necessário executar o seguinte comando como administrador para extrair os dumps:

 `python dump-extractor.py`

 # Análise dos Dumps de Memória
 
 **Sistemas usados para a análise: Ubuntu 20.04, Pop!OS**

 A análise dos dumps são feitas com o código em python `csv-maker.py`. Para rodar ele, é necessário configurar o ambiente do [Volatility](https://github.com/volatilityfoundation/volatility) e fazer o download do código [`VolatilityFeatureExtractor.py`](https://github.com/ahlashkari/VolMemLyzer). 

 ### Configurando o ambiente do Volatility

 * Instalando dependências do sistema

    `sudo apt install -y build-essential git libdistorm3-dev yara libraw1394-11        libcapstone-dev capstone-tool tzdata`

 * Instalando pip para o Python2

    `sudo apt install -y python2 python2.7-dev libpython2-dev`

    `curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py`

    `sudo python2 get-pip.py`

    `sudo python2 -m pip install -U setuptools wheel`

* Instalando Volatility2 e suas depências do Python

    `python2 -m pip install -U distorm3 yara pycrypto pillow openpyxl ujson pytz ipython capstone sudo python2 -m pip install yara`

    `sudo ln -s /usr/local/lib/python2.7/dist-packages/usr/lib/libyara.so /usr/lib/libyara.so`


    ### Clone o repositório do Volatility

    `git clone https://github.com/volatilityfoundation/volatility.git`

    Altere as permissões do arquivo `vol.py` e torne ele executável

    `chmod +x volatility/vol.py`

    Adicione o trecho de código na primeira linha do programa `vol.py`

    `#!/usr/bin/env python2`

### Testando o Volatility

`python2.7 volatility/vol.py --info`

### VolatilityFeatureExtractor

Para o `csv-maker.py` rodar corretamente, faça o download do código `VolatilityFeatureExtractor.py` e troque esse trecho do código:

```
if __name__ == '__main__':
    p, args = parse_args()
    if not os.path.isfile(args.memdump):
        p.error('Specified memory dump does not exist or is not a file.')
	# Enter file path here
    for filename in os.listdir('/home/'):
        if filename.endswith('.raw'):
		# Enter file path here
                path_in_str = os.path.join('/home/', filename)
                extract_all_features_from_memdump(path_in_str, args.output, args.volatility_exe)
```

por esse:

```
if __name__ == '__main__':
    p, args = parse_args()
    if not os.path.isfile(args.memdump):
        p.error('Specified memory dump does not exist or is not a file.')

    extract_all_features_from_memdump(args.memdump, args.output, args.volatility_exe)

```

