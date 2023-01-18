/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class', // class, 'media' or boolean
  theme: {
    extend: {
      colors: {
        gray: {
          900: '#202225',
          800: '#2f3136',
          700: '#36393f',
          600: '#4f545c',
          400: '#d4d7dc',
          300: '#e3e5e8',
          200: '#ebedef',
          100: '#f2f3f5',
        },
        'morp': '#f6f7f9',
        'muted': '#abb3bf',
        'primary': '#184A90',
        'primary-d': '#4C90F0',
      },
      spacing: {
        88: '22rem',
      },
    },
  },
  plugins: [],
}
