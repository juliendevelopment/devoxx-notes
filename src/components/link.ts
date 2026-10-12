/** Prefix a site path ("2026/notes/x") with the configured base. */
export const href = (path: string) =>
  `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\/|\/$/g, '')}/`;
