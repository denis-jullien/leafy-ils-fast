import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import type { Config } from 'tailwindcss';

export default {
	darkMode: 'class',
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		//👇 add Sara UI
		'./node_modules/saraui/**/*.{html,js,svelte,ts}'
	],

	theme: {
		extend: {}
	},

	plugins: [typography, forms, require('daisyui')],
	daisyui: {
		themes: ['emerald']
	}
} satisfies Config;
