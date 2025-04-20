import { ProgramBox, ProgramContent, ProgramStack, ProgramTitle, ProgramText, useProgram } from 'planby'
import '@styles/ProgramItem.css'

// Componente para renderizar un programa
export const ProgramItem = ({ program, onClick, ...rest }) => {
    const { styles, formatTime, isLive } = useProgram({ program, ...rest })
    const { data } = program
    const { title, since, till } = data

    const sinceTime = formatTime(since)
    const tillTime = formatTime(till)

    return (
        <ProgramBox style={styles.position} onClick={onClick}>
            <ProgramContent className="program-content" width={styles.width} isLive={isLive}>
                <ProgramStack className="program-stack">
                    <ProgramTitle>{title}</ProgramTitle>
                    <ProgramText>{sinceTime} - {tillTime}</ProgramText>
                </ProgramStack>
            </ProgramContent>
        </ProgramBox>
    )
}