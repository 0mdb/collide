import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App'
import './index.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

import ScrollToTop from './components/ScrollToTop'
import { AuthProvider } from 'react-auth-kit'
const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  // <React.StrictMode>

  <AuthProvider authType='localstorage' authName='_auth'>
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <ScrollToTop>
          <Routes>
            <Route path='/*' element={<App />} />
          </Routes>
          <ReactQueryDevtools />
        </ScrollToTop>
      </QueryClientProvider>
    </BrowserRouter>
  </AuthProvider>,
  // </React.StrictMode>,
)
