import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import TVGuide from './components/TVGuide'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <TVGuide />
  </StrictMode>,
)
