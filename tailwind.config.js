/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html", "./**/forms/**/*.py"],
  theme: {
    extend: {
      colors:{
        'blue-1': '#04ADBF',
        'blue-2': '#04BFBF',
        'green-3': '#025959',
        'green-4': '#A0A603',
        'vanilla-5': '#F2E0C9',
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
  // text-2xl or above will be ineffective due to Django template engine
  // thus we need to explicity state the attributes we want to have here
  purge: {
    options: {
      safelist: {
        standard: [
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
      },
    },
  }
}

