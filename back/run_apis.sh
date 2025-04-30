#!/bin/bash

# Executa cada API Flask em segundo plano
python Marketplace/marketplace.py &
python SNServicesMock/SNServicesMock.py &
python SNManager/support_network_manager.py &

# Aguarda todos os processos em segundo plano terminarem (opcional)
wait
