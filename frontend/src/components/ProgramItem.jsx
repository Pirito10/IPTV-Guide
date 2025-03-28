import { useState } from "react"
import { ProgramBox, ProgramContent, ProgramStack, ProgramTitle, ProgramText, useProgram } from 'planby'

// Componente para renderizar un programa
export const ProgramItem = ({ program, onClick, ...rest }) => {
    const { styles, formatTime, isLive } = useProgram({ program, ...rest })
    const { data } = program
    const { title, since, till } = data

    const sinceTime = formatTime(since)
    const tillTime = formatTime(till)

    // Estado para controlar el hover sobre los programas
    const [isHovered, setIsHovered] = useState(false)

    return (
        <ProgramBox
            width={styles.width}
            style={styles.position}
            onClick={onClick}
        >
            <ProgramContent
                // Añadimos los eventos para actualizar el hover
                width={styles.width}
                isLive={isLive}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                style={{ cursor: "pointer" }}
            >
                <ProgramStack
                    // Añadimos un efecto de zoom al pasar el ratón
                    style={{
                        transition: 'transform 0.2s',
                        transform: isHovered ? 'scale(1.025)' : 'scale(1)'
                    }}
                >
                    <ProgramTitle>{title}</ProgramTitle>
                    <ProgramText>{sinceTime} - {tillTime}</ProgramText>
                </ProgramStack>
            </ProgramContent>
        </ProgramBox >
    )
}