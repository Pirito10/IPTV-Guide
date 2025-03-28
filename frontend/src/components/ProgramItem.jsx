import { ProgramBox, ProgramContent, ProgramStack, ProgramTitle, ProgramText, useProgram } from 'planby'

// Componente para renderizar un programa
export const ProgramItem = ({ program, ...rest }) => {
    const { styles, formatTime, isLive } = useProgram({ program, ...rest })
    const { data } = program
    const { title, since, till } = data

    const sinceTime = formatTime(since)
    const tillTime = formatTime(till)

    // Eliminamos la imagen de los programas en directo
    return (
        <ProgramBox width={styles.width} style={styles.position}>
            <ProgramContent width={styles.width} isLive={isLive} style={{ cursor: "pointer" }}>
                    <ProgramStack>
                        <ProgramTitle>{title}</ProgramTitle>
                        <ProgramText>
                            {sinceTime} - {tillTime}
                        </ProgramText>
                    </ProgramStack>
            </ProgramContent>
        </ProgramBox>
    )
}