import { base } from '$app/paths';

export async function load({ fetch }) {
  let ellGraduation = { type: 'FeatureCollection', features: [] };
  let nyState = { type: 'FeatureCollection', features: [] };

  let suppressedSchools = [];

  const [ellRes, nyRes, suppressedRes] = await Promise.all([
    fetch(`${base}/data/ell-graduation.geojson`),
    fetch(`${base}/data/ny-state.geojson`),
    fetch(`${base}/data/suppressed-schools.json`),
  ]);

  if (ellRes.ok) ellGraduation = await ellRes.json();
  if (nyRes.ok) nyState = await nyRes.json();
  if (suppressedRes.ok) suppressedSchools = await suppressedRes.json();

  return {
    showHeader: true,
    showFooter: true,
    ellGraduation,
    nyState,
    suppressedSchools,
  };
}
