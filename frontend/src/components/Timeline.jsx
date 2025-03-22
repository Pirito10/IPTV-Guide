import {
    TimelineWrapper,
    TimelineBox,
    TimelineTime,
    TimelineDivider,
    TimelineDividers,
    useTimeline
} from "planby";

export function Timeline({
    isBaseTimeFormat,
    isSidebar,
    dayWidth,
    hourWidth,
    numberOfHoursInDay,
    offsetStartHoursRange,
    sidebarWidth
}) {
    const { time, dividers, formatTime } = useTimeline(
        numberOfHoursInDay,
        isBaseTimeFormat
    );

    const renderTime = (index) => (
        <TimelineBox key={index} width={hourWidth}>
            <TimelineTime>
                {formatTime(index + offsetStartHoursRange).toLowerCase()}
            </TimelineTime>
            <TimelineDividers>{renderDividers()}</TimelineDividers>
        </TimelineBox>
    );

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
        ));

    // Añadimos un marcador para la hora actual
    const renderNowIndicator = () => {
        // Calculamos la hora actual
        const now = new Date();
        const currentHour = now.getHours();
        const currentMinutes = now.getMinutes();
        const totalHours = currentHour + currentMinutes / 60;

        // Calculamos la posición del marcador en píxeles
        const left = totalHours * hourWidth;

        return (
            <div
                style={{
                    position: 'absolute',
                    left: `${left}px`,
                    bottom: '6px',
                    height: '14px',
                    width: '3px',
                    backgroundColor: '#2C7A7B'
                }}
            />
        );
    };

    return (
        <TimelineWrapper
            dayWidth={dayWidth}
            sidebarWidth={sidebarWidth}
            isSidebar={isSidebar}
        >
            {time.map((_, index) => renderTime(index))}
            {renderNowIndicator()}
        </TimelineWrapper>
    );
}