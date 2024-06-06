/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: false,
  content: [
    "./public/index.html",     
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};