# ✅ TODO list del proyecto

## 🔧 Backend
- [x] Fix: si no se descargó la lista de canales, la guía EPG se descarga y al filtrar por los canales queda vacía. Aunque entre un usuario y se descargue correctamente la lista de canales, la EPG no se vuelve a descargar hasta su timer, pues no dió error. Añadir caché permanente?
- [x] Añadir logo de cada canal a la guía EPG
- [x] Logger
- [x] Añadir timer de M3U a config.py
- [x] No parsear programas si el ID no está en la lista
- [ ] Almacenamiento local, varias copias?
- [ ] Gestión de errores
- [ ] Loguear requests
- [x] Añadir jitter a la caché de los logos

## 🖥️ Frontend
- [x] Mostrar tooltip al copiar un ID de stream
- [x] Cerrar el modal de canal al hacer click fuera
- [x] Cerrar el modal de canal al presionar escape
- [x] Editar estilo de ProgramItem
- [ ] Añadir instrucciones de uso
- [ ] Añadir filtrado por grupo
- [ ] Añadir buscador
- [ ] Revisar sincronización de la barra temporal
- [x] Mover estilos de los componentes a un .css
- [x] Modal para cada programa
- [x] onError en los modales

## 🧪 Extras
- [x] Si un canal no tiene logo o al cargarlo da error, asignarle su correspondiente de la guía EPG
- [x] Si es un canal sin ID -> imagen de respaldo
- [x] Eliminar puntos y coma
- [ ] Testear rendimiento de get_valid_logo() en la Raspberry
    - [x] Cachear logos validados