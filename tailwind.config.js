/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [

      "./**/templates/**/*.html",
      "./**/templates/**/*.jinja",
      "./**/static/**/*.js",
      "./**/*.py",
  ],
  safelist: [
    'text-2xl',
    'text-3xl',
    'text-4xl',
    'text-5xl',
    'text-6xl',
    'sm:text-2xl',
    'sm:text-3xl',
    'sm:text-4xl',
    'sm:text-5xl',
    'sm:text-6xl',
    'md:text-2xl',
    'md:text-3xl',
    'md:text-4xl',
    'md:text-5xl',
    'md:text-6xl',
    'lg:text-2xl',
    'lg:text-3xl',
    'lg:text-4xl',
    'lg:text-5xl',
    'lg:text-6xl',
  ],
  theme: {
    extend: {
      colors: {
        'blue-1': '#04ADBF',
        'blue-2': '#04BFBF',
        'green-3': '#025959',
        'green-4': '#A0A603',
        'vanilla-5': '#F2E0C9',
        'red-6': '#F23030',
        'vanilla-7': '#F2B680',
        'orange-8': '#E86C0C',
        'orange-9': '#F2C10C',

      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0px)' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0px)' },
        }
      },
      animation: {
        fadeUp: 'fadeUp 0.6s ease',
        fadeIn: 'fadeIn 0.6s ease'
      },
    },
  },
  plugins: [
    require('daisyui'),
    require('@tailwindcss/typography'),
  ],
};