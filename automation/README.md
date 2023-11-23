

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




