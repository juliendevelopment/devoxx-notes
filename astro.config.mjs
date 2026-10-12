// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sidebar from './src/sidebar.json' with { type: 'json' };

// Published on GitHub Pages at https://juliendevelopment.github.io/devoxx-notes/
// `base` must match BASE in sync.py.
export default defineConfig({
  site: 'https://juliendevelopment.github.io',
  base: '/devoxx-notes',
  integrations: [
    starlight({
      title: 'Devoxx notes',
      description: "Julien's takeaways and raw talk notes from Devoxx Belgium.",
      favicon: '/favicon.svg',
      customCss: [
        '@fontsource-variable/inter',
        '@fontsource-variable/space-grotesk',
        './src/styles/custom.css',
      ],
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/juliendevelopment/devoxx-notes' },
        { icon: 'youtube', label: 'Devoxx Belgium 2026 playlist', href: 'https://www.youtube.com/playlist?list=PLKlmOVksNGoE' },
      ],
      sidebar,
    }),
  ],
});
