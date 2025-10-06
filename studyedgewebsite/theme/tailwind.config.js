/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static_src/js/**/*.js',
  ],
  darkMode: 'class', // <-- important
  theme: {
    extend: {},
  },
  plugins: [],
}
