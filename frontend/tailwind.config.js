/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'Segoe UI', 'sans-serif']
      },
      colors: {
        graphite: {
          950: '#06100d',
          900: '#0a1613',
          850: '#10201c',
          800: '#172b26'
        },
        agri: {
          50: '#eafff5',
          100: '#c9ffe4',
          300: '#71efad',
          400: '#34d987',
          500: '#12b76a',
          600: '#079455',
          700: '#067647'
        },
        orbit: {
          400: '#38bdf8',
          500: '#0ea5e9'
        }
      },
      boxShadow: {
        glass: '0 18px 60px rgba(0, 0, 0, 0.25)',
        glow: '0 0 34px rgba(18, 183, 106, 0.24)'
      },
      backgroundImage: {
        'farm-hero':
          "linear-gradient(90deg, rgba(4, 12, 10, 0.78), rgba(4, 12, 10, 0.42), rgba(4, 12, 10, 0.12)), url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1800&q=80')"
      }
    }
  },
  plugins: []
};
