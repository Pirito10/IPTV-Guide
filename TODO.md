# ✅ TODO list del proyecto

## 🔧 Backend
- [ ] Fix: si no se descargó la lista de canales, la guía EPG se descarga y al filtrar por los canales queda vacía. Aunque entre un usuario y se descargue correctamente la lista de canales, la EPG no se vuelve a descargar hasta su timer, pues no dió error. Añadir caché permanente?
- [x] Añadir logo de cada canal a la guía EPG
- [ ] Logger
- [ ] Añadir timer de M3U a config.py

## 🖥️ Frontend
- [ ] Mostrar tooltip al copiar un ID de stream
- [x] Cerrar el modal de canal al hacer click fuera
- [x] Cerrar el modal de canal al presionar escape
- [ ] Editar estilo de ProgramItem
- [ ] Añadir instrucciones de uso
- [ ] Añadir filtrado por grupo
- [ ] Añadir buscador

## 🧪 Extras
- [x] Si un canal no tiene logo o al cargarlo da error, asignarle su correspondiente de la guía EPG
- [x] Si es un canal sin ID -> imagen de respaldo
- [ ] Eliminar puntos y coma
- [ ] Testear rendimiento de get_valid_logo() en la Raspberry
    - [ ] Cachear logos validados