/** @type {import('tailwindcss').Config} */

const colors = require('tailwindcss/colors')
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class', // class, 'media' or boolean
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        gray: {  // slate
          900: '#0f172a',
          800: '#1e293b',
          700: '#334155',
          600: '#475569',
          400: '#94a3b8',
          300: '#cbd5e1',
          200: '#e2e8f0',
          100: '#f1f5f9',
        },
        'morp': '#f6f7f9',  // nearly white
        'muted': '#abb3bf',  // light gray

        'primary': '#4338ca',  // indigo-700
        'primary-l': '#818cf8',  // indigo-400
        'primary-d': '#312e81',  // indigo-900

        'secondary': '#64748b',  // slate-500
        'secondary-l': '#cbd5e1',  // slate-300
        'secondary-d': '#334155',  // slate-700

        'primary-text': '#ffffff',  // white
        'primary-l-text': '#000000',  // black
        'primary-d-text': '#ffffff',  // white

//         'primary-text-accent':
//         'primary-l-text-accent':
//         'primary-d-text-accent':
//
//         'primary-text-accent-hov':
//         'primary-l-text-accent-hov':
//         'primary-d-text-accent-hov':

        'secondary-text': '#ffffff',  // white
        'secondary-l-text': '#000000',  // black
        'secondary-d-text': '#ffffff',  // white

        'secondary-accent': '#4338ca',  // indigo-700
        'secondary-l-accent': '#312e81',  // indigo-900
        'secondary-d-accent': '#818cf8',  // indigo-400

        'secondary-accent-hov': '#818cf8',  // indigo-400
        'secondary-l-accent-hov': '#6366f1'  // indigo-500
        'secondary-d-accent-hov': '#312e81',  // indigo-900

        'analogous1': '#8d38ca',  // magenta
        'analogous2': '#38b4ca',  // teal
      },
      // spacing: {
      //   88: '22rem',
      // },
    },
  },
    plugins: [
      require('@tailwindcss/typography'),
      require('@tailwindcss/forms'),
      // require('@tailwindcss/line-clamp'),
      // require('@tailwindcss/aspect-ratio'),
  ],
};
