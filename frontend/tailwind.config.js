/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#16a34a',
        'primary-light': '#22c55e',
        'primary-dark': '#15803d',
        secondary: '#64748b',
        accent: '#f43f5e',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
