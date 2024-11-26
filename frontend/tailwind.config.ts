import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import type { Config } from 'tailwindcss';

// 1. Import the Skeleton plugin
import { join } from 'path';
import { skeleton } from '@skeletonlabs/tw-plugin';

export default {
	// 2. Opt for dark mode to be handled via the class method
	darkMode: 'class',
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		// 3. Append the path to the Skeleton package
		join(require.resolve(
				'@skeletonlabs/skeleton'),
			'../**/*.{html,js,svelte,ts}'
		)
	],

	theme: {
		extend: {}
	},

	plugins: [
		typography, forms,
		skeleton({
			themes: { preset: [ "skeleton" ] }
		})
	]
} satisfies Config;
