export async function load({ fetch }) {
  let ellGraduation = { type: 'FeatureCollection', features: [] };
  let nyState = { type: 'FeatureCollection', features: [] };

  let suppressedSchools = [];

  const [ellRes, nyRes, suppressedRes] = await Promise.all([
    fetch('/data/ell-graduation.geojson'),
    fetch('/data/ny-state.geojson'),
    fetch('/data/suppressed-schools.json'),
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
