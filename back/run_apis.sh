#!/bin/bash

# Executa cada API Flask em segundo plano
C:/Users/Matheus/AppData/Local/Programs/Python/Python313/python.exe marketplace.py &
C:/Users/Matheus/AppData/Local/Programs/Python/Python313/python.exe examples/components/template/SNServicesMock.py &
C:/Users/Matheus/AppData/Local/Programs/Python/Python313/python.exe support_network_manager.py &

# Aguarda todos os processos em segundo plano terminarem (opcional)
wait
