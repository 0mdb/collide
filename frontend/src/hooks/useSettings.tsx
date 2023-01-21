import useLocalStorage from './useLocalStorage'

function useSettings() {
  const [settings, setSettings] = useLocalStorage('settings', {
    language: 'en',
    theme: 'light',
  })

  const updateSettings = (newSettings) => {
    setSettings({ ...settings, ...newSettings })
  }

  return { settings, updateSettings }
}

export default useSettings
