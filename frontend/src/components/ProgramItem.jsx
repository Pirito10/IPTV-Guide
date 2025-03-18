import { ProgramBox, ProgramContent, ProgramFlex, ProgramStack, ProgramTitle, ProgramText, useProgram } from 'planby'

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
            <ProgramContent width={styles.width} isLive={isLive}>
                <ProgramFlex>
                    <ProgramStack>
                        <ProgramTitle>{title}</ProgramTitle>
                        <ProgramText>
                            {sinceTime} - {tillTime}
                        </ProgramText>
                    </ProgramStack>
                </ProgramFlex>
            </ProgramContent>
        </ProgramBox>
    )
}