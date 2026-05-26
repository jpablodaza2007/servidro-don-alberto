#!/bin/bash

echo "Iniciando el despliegue automatico de Peritajes"

# Ir a la carpeta del proyecto
cd /var/www/html

# Traer cambios desde GitHub
echo "Trayendo la ultima version desde git"
git pull origin main

# Reiniciar servicio systemd
echo "Reiniciando servicio Flask"
sudo systemctl restart peritajes.service

# Mostrar estado
echo "Despliegue completado. Estado actual:"
sudo systemctl status peritajes.service | grep "Active:"
