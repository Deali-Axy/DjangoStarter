/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './src/**/templates/**/*.html',
        './src/static/lib/flowbite/**/*.js',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('flowbite/plugin'),
    ],
}

