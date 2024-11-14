#!/bin/bash

# Executa cada API Flask em segundo plano
python marketplace.py &
python examples/components/template/SNServicesMock.py &
python support_network_manager.py &

# Aguarda todos os processos em segundo plano terminarem (opcional)
wait
