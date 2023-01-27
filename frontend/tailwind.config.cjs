/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class', // class, 'media' or boolean
  theme: {
    extend: {
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
        'primary-l': '#6366f1',  // indigo-500
        'primary-d': '#312e81',  // indigo-900
        'secondary': '#64748b',  // slate-500
        'secondary-l': '#cbd5e1',  // slate-300
        'secondary-d': '#334155',  // slate-700
        'primary-text': '#ffffff',  // white
        'secondary-text': '#ffffff',  // white
        'analogous1': '#8d38ca',  // magenta
        'analogous2': '#38b4ca'  // teal
      },
      // spacing: {
      //   88: '22rem',
      // },
    },
  },
    plugins: [
      // require('@tailwindcss/typography'),
      // require('@tailwindcss/forms'),
      // require('@tailwindcss/line-clamp'),
      // require('@tailwindcss/aspect-ratio'),
  ],
};
