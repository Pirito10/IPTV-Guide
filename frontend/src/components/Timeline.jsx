import { TimelineWrapper, TimelineBox, TimelineTime, TimelineDivider, TimelineDividers, useTimeline } from 'planby'
import '@styles/Timeline.css'

export const Timeline = ({ isBaseTimeFormat, dayWidth, hourWidth, numberOfHoursInDay, offsetStartHoursRange, sidebarWidth }) => {
    const { time, dividers, formatTime } = useTimeline(numberOfHoursInDay, isBaseTimeFormat)

    // Función para calcular la clase de los divisores
    const getDividerClass = index => {
        if (index % 4 === 0) return "divider-full-hour" // En punto
        if (index % 2 === 0) return "divider-half-hour" // Media hora
        return "divider-quarter-hour" // Cuarto/tres cuartos de hora
    }

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
                className={`${getDividerClass(index)}`} // Modificamos la altura de los divisores en función de la hora
            />
        ))

    return (
        <TimelineWrapper dayWidth={dayWidth} sidebarWidth={sidebarWidth}>
            {time.map((_, index) => renderTime(index))}
        </TimelineWrapper>
    )
}