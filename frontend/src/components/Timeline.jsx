import { useEffect, useState } from 'react'
import { TimelineWrapper, TimelineBox, TimelineTime, TimelineDivider, TimelineDividers, useTimeline } from 'planby'
import '@styles/Timeline.css'

export const Timeline = ({ isBaseTimeFormat, isSidebar, dayWidth, hourWidth, numberOfHoursInDay, offsetStartHoursRange, sidebarWidth }) => {
    const { time, dividers, formatTime } = useTimeline(numberOfHoursInDay, isBaseTimeFormat)

    // Estado para guardar la hora actual y actualizarla automáticamente cada minuto
    const [now, setNow] = useState(new Date())
    useEffect(() => {
        const updateNow = () => setNow(new Date())
        // Forzamos una actualización al montar el componente
        updateNow()
        // Actualizamos cada dos minutos
        const interval = setInterval(updateNow, 120000)
        return () => clearInterval(interval)
    }, [])

    const renderTime = (index) => (
        <TimelineBox key={index} width={hourWidth}>
            <TimelineTime>
                {formatTime(index + offsetStartHoursRange).toLowerCase()}
            </TimelineTime>
            <TimelineDividers>{renderDividers()}</TimelineDividers>
        </TimelineBox>
    )

    const renderDividers = () =>
        dividers.map((_, index) => (
            <TimelineDivider
                key={index}
                width={hourWidth}
                // Modificamos la altura de los divisores en función de la hora
                style={{
                    height:
                        index % 4 === 0 ? '25%' : // En punto
                            index % 2 === 0 ? '18%' : // Media hora
                                '10%', // Cuarto/tres cuartos de hora
                }}
            />
        ))

    // Añadimos un marcador para la hora actual
    const renderNowIndicator = () => {
        // Calculamos la hora actual
        const currentHour = now.getHours()
        const currentMinutes = now.getMinutes()
        const totalHours = currentHour + currentMinutes / 60

        // Calculamos la posición del marcador en píxeles
        const left = totalHours * hourWidth

        return (
            <div className="timeline-now-indicator" style={{ left: `${left}px` }} />
        )
    }

    return (
        <TimelineWrapper
            dayWidth={dayWidth}
            sidebarWidth={sidebarWidth}
            isSidebar={isSidebar}
        >
            {time.map((_, index) => renderTime(index))}
            {renderNowIndicator()}
        </TimelineWrapper>
    )
}