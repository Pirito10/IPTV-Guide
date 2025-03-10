import React, { useEffect, useState } from 'react'

function App() {
  const [channels, setChannels] = useState([])
  const [epg, setEpg] = useState([])

  useEffect(() => {
    // Obtener lista de canales
    fetch('http://localhost:5000/api/channels')
      .then((res) => res.json())
      .then((data) => setChannels(data))
      .catch((error) => console.error("Error obteniendo canales:", error))

    // Obtener guía EPG
    fetch('http://localhost:5000/api/epg')
      .then((res) => res.json())
      .then((data) => setEpg(data))
      .catch((error) => console.error("Error obteniendo EPG:", error))
  }, [])

  return (
    <div>
      <h1>Guía de TV</h1>
      <table border="1">
        <thead>
          <tr>
            <th>Canal</th>
            <th>Programas</th>
          </tr>
        </thead>
        <tbody>
          {channels.map((channel) => (
            <tr key={channel.tvg_id}>
              <td>{channel.name}</td>
              <td>
                {epg[channel.tvg_id] ? (
                  epg[channel.tvg_id].map((program, index) => (
                    <div key={index}>
                      {program.title} ({program.start} - {program.stop})
                    </div>
                  ))
                ) : (
                  "Sin programación"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App