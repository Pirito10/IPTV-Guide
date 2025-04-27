# ✅ TODO list del proyecto

## 🔧 Backend
- [x] Fix: si no se descargó la lista de canales, la guía EPG se descarga y al filtrar por los canales queda vacía. Aunque entre un usuario y se descargue correctamente la lista de canales, la EPG no se vuelve a descargar hasta su timer, pues no dió error. Añadir caché permanente?
- [x] Añadir logo de cada canal a la guía EPG
- [x] Logger
- [x] Añadir timer de M3U a config.py
- [x] No parsear programas si el ID no está en la lista
- [x] Cachear logos validados
- [x] Almacenamiento local, varias copias?
- [x] Gestión de errores
- [x] Añadir jitter a la caché de los logos
- [ ] Tests
- [x] Exclusión mutua para update_m3u
- [x] Cachear logos inválidos si hay problemas de rendimiento para evitar esperar al timeout por cada logo inválido
- [ ] Loguear requests (probar en producción sobre el servidor nginx)

## 🖥️ Frontend
- [x] Mostrar tooltip al copiar un ID de stream
- [x] Cerrar el modal de canal al hacer click fuera
- [x] Cerrar el modal de canal al presionar escape
- [x] Editar estilo de ProgramItem
- [x] Añadir instrucciones de uso
- [x] Añadir filtrado por grupo
- [ ] Añadir buscador
- [x] Revisar sincronización de la barra temporal
- [x] Mover estilos de los componentes a un .css
- [x] Modal para cada programa
- [x] onError en los modales
- [x] Animaciones "active" para los botones
- [x] Revisar handlers para click fuera de modal
- [x] Animaciones para los modales
- [ ] Completar los TODO de InfoModal.jsx

## ✨ Extras
- [x] Si un canal no tiene logo o al cargarlo da error, asignarle su correspondiente de la guía EPG
- [x] Si es un canal sin ID -> imagen de respaldo
- [x] Eliminar puntos y coma

## 🧪 Testing
- [ ] Testear rendimiento de get_valid_logo() en la Raspberry
- [ ] Testear botón de copiar ID sobre HTTPS