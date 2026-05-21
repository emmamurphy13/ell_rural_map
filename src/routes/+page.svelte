<script>
  import { onMount } from 'svelte';
  import ArticleHeader from '$lib/components/Article/ArticleHeader.svelte';
  import Map from '$lib/components/Maps/Map.svelte';
  import MapLayer from '$lib/components/Maps/MapLayer.svelte';
  import Legend from '$lib/components/Maps/Legend.svelte';

  onMount(() => {
    window.addEventListener('message', function(e) {
      if (e.data['datawrapper-height'] !== undefined) {
        const iframes = document.querySelectorAll('iframe');
        for (const id in e.data['datawrapper-height']) {
          for (const iframe of iframes) {
            if (iframe.contentWindow === e.source) {
              iframe.style.height = e.data['datawrapper-height'][id] + 'px';
            }
          }
        }
      }
    });
  });

  let { data } = $props();
  const ellGraduation = data.ellGraduation;
  const nyState = data.nyState;
  const suppressedSchools = data.suppressedSchools;

  let hoveredSchool = $state(null);
  let tooltipX = $state(0);
  let tooltipY = $state(0);

  const ALL_LOCALES = ['City', 'Suburb', 'Town', 'Rural'];

  const LOCALE_DEFS = {
    City: [
      { name: 'Large', desc: 'Territory inside a principal city with a population of 250,000 or more.' },
      { name: 'Midsize', desc: 'Territory inside a principal city with a population of 100,000 to 250,000.' },
      { name: 'Small', desc: 'Territory inside a principal city with a population less than 100,000.' },
    ],
    Suburb: [
      { name: 'Large', desc: 'Territory outside a principal city in an urbanized area with a population of 250,000 or more.' },
      { name: 'Midsize', desc: 'Territory outside a principal city in an urbanized area with a population of 100,000 to 250,000.' },
      { name: 'Small', desc: 'Territory outside a principal city in an urbanized area with a population of 50,000 to 100,000.' },
    ],
    Town: [
      { name: 'Fringe', desc: 'Territory in an urban cluster up to 10 miles from an urbanized area.' },
      { name: 'Distant', desc: 'Territory in an urban cluster 10 to 35 miles from an urbanized area.' },
      { name: 'Remote', desc: 'Territory in an urban cluster more than 35 miles from an urbanized area.' },
    ],
    Rural: [
      { name: 'Fringe', desc: 'Census-defined rural territory up to 5 miles from an urbanized area or 2.5 miles from an urban cluster.' },
      { name: 'Distant', desc: 'Census-defined rural territory 5 to 25 miles from an urbanized area or 2.5 to 10 miles from an urban cluster.' },
      { name: 'Remote', desc: 'Census-defined rural territory more than 25 miles from an urbanized area or more than 10 miles from an urban cluster.' },
    ],
  };

  let activeLocaleTab = $state('City');
  let activeLocales = $state(new Set(ALL_LOCALES));

  function toggleLocale(locale) {
    const next = new Set(activeLocales);
    if (next.has(locale)) next.delete(locale);
    else next.add(locale);
    activeLocales = next;
  }

  // Filter for map display: valid grad rate + selected locales
  const localeFilter = $derived.by(() => {
    const hasGrad = ['>', ['get', 'per_grad'], 0];
    if (activeLocales.size === 0) return ['in', ['get', 'locale'], ['literal', []]]; // show nothing
    if (activeLocales.size === ALL_LOCALES.length) return hasGrad;
    return ['all', hasGrad, ['in', ['get', 'locale'], ['literal', [...activeLocales]]]];
  });

  // Count only dots shown on map (have geometry + valid grad rate + selected locale)
  const displayedCount = $derived(
    ellGraduation.features.filter(f =>
      f.geometry &&
      f.properties.per_grad > 0 &&
      activeLocales.has(f.properties.locale)
    ).length
  );

  const stats = $derived.by(() => {
    let totalGrads = 0;
    let totalDropouts = 0;
    let totalEnrolled = 0;
    for (const f of ellGraduation.features) {
      const p = f.properties;
      if (!activeLocales.has(p.locale)) continue;
      if (!p.total_enrolled) continue;
      // All enrolled go into denominator (matches notebook .sum(min_count=1))
      totalEnrolled += p.total_enrolled;
      if (p.num_grad != null) totalGrads += p.num_grad;
      if (p.num_dropout != null) totalDropouts += p.num_dropout;
    }
    return {
      avgGrad: totalEnrolled ? ((totalGrads / totalEnrolled) * 100).toFixed(1) : '—',
      avgDropout: totalEnrolled ? ((totalDropouts / totalEnrolled) * 100).toFixed(1) : '—',
    };
  });

  let searchQuery = $state('');
  let selectedSchool = $state(null);

  const searchResults = $derived.by(() => {
    if (selectedSchool) return [];
    const q = searchQuery.trim().toLowerCase();
    if (!q) return [];
    return suppressedSchools.filter(s =>
      s.name.toLowerCase().includes(q) || s.city.toLowerCase().includes(q)
    ).slice(0, 8);
  });

  let pinnedSchool = $state(null);
  let pinnedX = $state(0);
  let pinnedY = $state(0);

  function handleMousemove(e) {
    if (!e.features?.length) return;
    const props = e.features[0].properties;
    hoveredSchool = props;
    tooltipX = e.originalEvent.offsetX;
    tooltipY = e.originalEvent.offsetY;
  }

  function handleMouseleave() {
    hoveredSchool = null;
  }

  function handleClick(feature) {
    pinnedSchool = feature.properties;
    pinnedX = tooltipX;
    pinnedY = tooltipY;
  }

  const displaySchool = $derived(hoveredSchool ?? pinnedSchool);
  const displayX = $derived(hoveredSchool ? tooltipX : pinnedX);
  const displayY = $derived(hoveredSchool ? tooltipY : pinnedY);
</script>

<svelte:window onclick={() => { pinnedSchool = null; }} />

<div class="container">
  <div class="article-kicker">New York</div>
  <ArticleHeader
    headline="English Language Learners in Rural New York schools face hurdles to graduate"
    byline="Emma Ferrara"
    pubDate="May 6, 2026, 5:54pm EDT"
  />

  <div class="share-bar">
    <a href="https://bsky.app/intent/compose?text=ELL+student+dropout+rates+across+New+York+State" class="share-link" aria-label="Share on Bluesky">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="#4a82c4"><path d="M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.204-.659-.3-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8Z"/></svg>
    </a>
    <a href="https://www.threads.net/intent/post?text=ELL+student+dropout+rates+across+New+York+State" class="share-link" aria-label="Share on Threads">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="#555"><path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.5 12.068c0-3.558.857-6.427 2.499-8.434C5.849 1.213 8.6.026 12.13.001h.015c2.745.021 5.1.787 7.008 2.279 1.77 1.38 2.977 3.292 3.588 5.684l-2.37.563c-1.034-4.084-3.823-6.264-8.234-6.264-2.898.021-5.063.937-6.453 2.723C4.406 6.637 3.78 9.09 3.78 12.068c0 3.018.627 5.48 1.875 7.32 1.39 1.783 3.553 2.697 6.432 2.718 2.553.019 4.275-.68 5.259-2.135.65-.963.958-2.127.921-3.452-.547.218-1.168.381-1.85.48-1.31.188-2.478.03-3.375-.46-.857-.462-1.426-1.225-1.569-2.132-.197-1.26.447-2.55 1.638-3.32.992-.638 2.313-.932 3.756-.852a13.27 13.27 0 0 1 1.476.192c-.083-.726-.295-1.306-.654-1.725-.467-.538-1.215-.812-2.226-.813h-.015c-.826 0-1.707.246-2.286.64L11.37 8.47c.875-.587 2.12-.91 3.395-.91h.024c1.558.007 2.828.497 3.678 1.416.77.837 1.175 1.993 1.266 3.507.075.026.147.056.218.088 1.293.592 2.115 1.698 2.115 2.953 0 .44-.097.854-.29 1.23a3.098 3.098 0 0 1-.837 1.025c.197.614.295 1.27.295 1.967 0 1.736-.43 3.23-1.279 4.439C19.743 23.108 17.382 24 14.33 24c-.725 0-1.445-.071-2.144-.211zm.765-7.916c.76-.11 1.454-.357 1.992-.656a9.1 9.1 0 0 0-.145-1.45 6.54 6.54 0 0 0-1.398-.167c-.957-.055-1.787.138-2.344.493-.409.263-.619.617-.543 1.094.07.449.331.752.774.997.586.316 1.297.388 1.664.389z"/></svg>
    </a>
    <a href="https://twitter.com/intent/tweet?url=https://chalkbeat.org" class="share-link" aria-label="Share on X">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="#555"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </a>
    <a href="https://www.facebook.com/sharer/sharer.php?u=https://chalkbeat.org" class="share-link" aria-label="Share on Facebook">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="#4a6fb5"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
    </a>
    <a href="https://reddit.com/submit?url=https://chalkbeat.org" class="share-link" aria-label="Share on Reddit">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="#555"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/></svg>
    </a>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://chalkbeat.org" class="share-link" aria-label="Share on LinkedIn">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="#4a6fb5"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
    </a>
    <a href="https://www.chalkbeat.org/pages/republishing/" class="share-republish">Republish</a>
  </div>

  <h2 class="map-subheadline">Compare School Districts</h2>

  <Legend
    title=""
    mode="categorical"
    items={[
      { color: '#1a9850', label: '75–100%' },
      { color: '#fee08b', label: '50–74%' },
      { color: '#fc8d59', label: '25–49%' },
      { color: '#d73027', label: '0–24%' },
    ]}
  />

  <div class="filter-bar">
    <span class="filter-label">Filter by locale:</span>
    {#each ALL_LOCALES as locale}
      <button
        class="filter-btn"
        class:active={activeLocales.has(locale)}
        onclick={() => toggleLocale(locale)}
      >{locale}</button>
    {/each}
    <button class="filter-btn deselect-btn" onclick={() => activeLocales = new Set()}>Deselect all</button>
  </div>

  <div class="stats-box">
    <div class="stat">
      <span class="stat-value">{stats.avgGrad}%</span>
      <span class="stat-label">Graduation rate for ELLs</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat stat-count">
      <span class="count-badge">{displayedCount}</span>
      <span class="stat-label">school{displayedCount !== 1 ? 's' : ''} shown</span>
    </div>
  </div>

  <div class="map-wrapper">
    <Map
      longitude={-75.8}
      latitude={42.9}
      zoom={6.5}
      aspectRatio="4 / 3"
      theme="positron"
      fitBounds={[[-80.5, 40.0], [-71.2, 45.6]]}
      maxBounds={[[-79.9, 40.4], [-71.7, 45.1]]}
      credit="OpenFreeMap / OpenStreetMap contributors · NYSED 2023-24"
    >
      <MapLayer
        id="ny-border"
        type="line"
        data={nyState}
        paint={{
          'line-color': '#000000',
          'line-width': 2,
          'line-opacity': 0.8,
        }}
      />
      <MapLayer
        id="ell-schools"
        type="circle"
        data={ellGraduation}
        paint={{
          'circle-radius': [
            'interpolate', ['linear'], ['get', 'total_enrolled'],
            0, 4,
            10, 5,
            50, 7,
            200, 10,
            500, 14,
          ],
          'circle-color': [
            'case',
            ['>=', ['get', 'per_grad'], 75], '#1a9850',
            ['>=', ['get', 'per_grad'], 50], '#fee08b',
            ['>=', ['get', 'per_grad'], 25], '#fc8d59',
            '#d73027',
          ],
          'circle-opacity': 0.85,
          'circle-stroke-width': 1,
          'circle-stroke-color': '#ffffff',
          'circle-stroke-opacity': 0.6,
        }}
        filter={localeFilter}
        onMousemove={handleMousemove}
        onMouseleave={handleMouseleave}
        onClick={handleClick}
      />
    </Map>

    {#if displaySchool}
      <div class="tooltip" class:is-pinned={pinnedSchool && !hoveredSchool} style:left="{displayX + 12}px" style:top="{displayY - 10}px" onclick={(e) => e.stopPropagation()}>
        {#if pinnedSchool && !hoveredSchool}
          <button class="tooltip-close" onclick={() => pinnedSchool = null} aria-label="Close">✕</button>
        {/if}
        <strong>{displaySchool.name}</strong><br />
        <span style="color: #666; font-size: 12px;">{displaySchool.city}, NY &middot; {displaySchool.locale}</span><br />
        {#if displaySchool.per_grad !== null}
          <span class="tt-label">Graduation rate:</span> {Number(displaySchool.per_grad).toFixed(1)}%<br />
          <span class="tt-label">High School ELL Enrollment:</span> {displaySchool.total_enrolled}<br />
          <span class="tt-label">ELL Enrollment K-12:</span> {displaySchool.k12_enrolled}<br />
          {#if displaySchool.home_languages && displaySchool.home_languages !== 'null'}
            <span class="tt-label">Languages:</span> {(typeof displaySchool.home_languages === 'string' ? JSON.parse(displaySchool.home_languages) : displaySchool.home_languages).join(', ')}
          {/if}
        {:else}
          Data suppressed (&lt;5 students)
        {/if}
      </div>
    {/if}
  </div>

  <div class="missing-school-section">
    <h3 class="missing-school-headline">Don't see your school?</h3>
    <p class="missing-school-body">To protect the identities of students, graduation data is suppressed when there are less than 5 English Language Learners in a school. These schools have been left off the map as a result of limited data.</p>
    <p class="missing-school-body"><strong>Still curious about a specific district? Use this database to see all available information:</strong></p>
    <div class="db-search-wrapper">
      <svg class="db-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="11" cy="11" r="8"/>
        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <input
        class="db-search"
        type="text"
        placeholder="Search by district or city name…"
        bind:value={searchQuery}
        oninput={() => selectedSchool = null}
      />
      {#if searchResults.length > 0}
        <ul class="db-results">
          {#each searchResults as school}
            <li>
              <button class="db-result-btn" onclick={() => { selectedSchool = school; searchQuery = school.name; }}>
                <span class="db-result-name">{school.name}</span>
                <span class="db-result-city">{school.city}, NY</span>
              </button>
            </li>
          {/each}
        </ul>
      {/if}
    </div>
    {#if selectedSchool}
      <div class="db-card-row-layout">
        <div class="db-card">
          <h4 class="db-card-name">{selectedSchool.name}</h4>
          <p class="db-card-location">{selectedSchool.city}, NY &middot; {selectedSchool.locale}</p>
          <dl class="db-card-stats">
            <div class="db-card-row">
              <dt>ELL Enrollment K-12:</dt>
              <dd>{selectedSchool.k12_enrolled}</dd>
            </div>
            <div class="db-card-row">
              <dt>High School ELL Enrollment:</dt>
              <dd>{selectedSchool.total_enrolled ?? 'Suppressed (fewer than 5 students)'}</dd>
            </div>
            {#if selectedSchool.home_languages?.length}
              <div class="db-card-row">
                <dt>Home languages:</dt>
                <dd>{selectedSchool.home_languages.join(', ')}</dd>
              </div>
            {/if}
          </dl>
        </div>
        {#if selectedSchool.lat && selectedSchool.lon}
          <div class="db-mini-map">
            {#key selectedSchool.name}
            <Map
              longitude={selectedSchool.lon}
              latitude={selectedSchool.lat}
              zoom={7}
              theme="positron"
              aspectRatio="1 / 1"
              credit=""
            >
              <MapLayer
                id="db-school-point"
                type="circle"
                data={{
                  type: 'FeatureCollection',
                  features: [{
                    type: 'Feature',
                    geometry: { type: 'Point', coordinates: [selectedSchool.lon, selectedSchool.lat] },
                    properties: {},
                  }],
                }}
                paint={{
                  'circle-radius': 8,
                  'circle-color': '#3370B8',
                  'circle-stroke-width': 2,
                  'circle-stroke-color': '#fff',
                }}
              />
            </Map>
            {/key}
          </div>
        {/if}
      </div>
    {/if}
  </div>

  <div class="article-body">
    <p>A young girl in upstate New York is waiting to see if she's allowed to take the one class that would allow her to graduate from high school on time. Her first language is Spanish, and her school district says her vocabulary isn't strong enough yet to enroll in Biology.</p>

    <p>Students in small towns and rural areas, like the girl, often migrate to the U.S. without their parents to work on farms and send money back home to their families. Some choose to attend schools, but it's not an easy transition. In some ways, even with her Biology struggles, the girl is lucky – she's learning English quickly, and she has adults advocating for her.</p>

    <p>"Her parents are here working, but her parents are afraid to make waves," said Mary Jo Dudley, former director of the Corell Farmerworkers program. "She reached out to me and so I've been trying to get a meeting with her guidance counselor for a month."</p>

    <p>While Dudley hasn't yet had success in getting her in the Biology class she needs, she has a lot of experience speaking up for migrants who are nervous about ruffling feathers in their new community.</p>

    <p>In the rural villages where Dudley primarily works, getting a high school diploma is especially challenging for English Language Learners. ELL students in New York cities and suburbs have a 50.6% graduation rate, but only 28.9% of students in rural areas or towns graduate in the standard four years. While there's no singular explanation for these statistics, one of the most obvious factors is that there are simply fewer kids who need help learning new languages in rural schools than in urban or suburban ones.</p>

    <iframe
      title="Cities have more experience educating ELLs"
      aria-label="Column Chart"
      id="datawrapper-chart-9o3vR"
      src="https://datawrapper.dwcdn.net/9o3vR/1/"
      scrolling="no"
      frameborder="0"
      style="width: 0; min-width: 100% !important; border: none;"
      height="437"
      data-external="1"
    ></iframe>

    <p>"When we need to think out of the box as to how to help that kid graduate, sometimes the decision makers in schools, they're not comfortable doing that.," said Beth Clark-Gareca, CCPA Department of Teaching, Learning and Educational Leadership at Binghamton University. "They've never had to do that before. They're afraid that they're going to break some sort of a rule."</p>

    <p>Schools with 20 students in the same grade who speak the same language at home are required to implement a bilingual education or dual language program, which often have better results educating students. Rural schools rarely meet this threshold, but they can still implement these programs if they choose.</p>

    <p>At suburban schools about 30% of students are in dual or bilingual programs, while only about 12% are at rural schools. The rest of the students still get a specialized education, but the English as a New Language courses don't place an emphasis on the student's native language and don't require the teacher to speak it.</p>

    <p>The students who migrate to small towns in upstate New York often have a different background than their counterparts in cities and could be in greater need of a bilingual program.</p>

    <p>"They're coming from communities where public education only goes to 6th grade," said Dudley. "And so in order to pursue education beyond 6th grade, if you're from those rural communities, your family has to have enough money to send you to a city and pay room and board."</p>

    <p>While the majority of English Language Learners speak Spanish at home, there is huge linguistic diversity across the state. Recent global conflicts have led to an influx of students from Ukraine and Myanmar, and six schools in New York have Latin American students who speak a Mayan language. Five of them are in rural areas. So even if a school has a bilingual program for Spanish students, it wouldn't be helpful for these immigrants.</p>

    <p>There are teaching methods designed for these sorts of situations.</p>

    <p>"Your classroom should be print-rich, and there should be visuals," said Myra Mora, retired school principal and bilingual teacher in upstate schools. "Any practice for English Language Learners is good practice."</p>

    <p>Mora says simple signs labeling items in the classroom also make a big difference.</p>

    <p>But rural schools outperform other schools only in one key category: dropout rates.</p>

    <p>Even these numbers, however, can distort and minimize the problem. While it may seem like a school with a poor graduation rate would also have a poor dropout rate, that isn't always the case. Students who don't graduate in four years won't be included in the drop out rate, and neither will students who transfer to other schools. In some cases, schools have been accused of using these loop holes to artificially lower their drop out rate.</p>

    <p>The young woman Dudley is working with, for example, won't have to drop out if she isn't allowed to take Biology. She can stay in school until she's reached a level of proficiency in English to take the course or until the end of the school year when she turns 21. But many students like her get discouraged or aren't able to spare the time.</p>

    <p>"If she can't graduate from high school, then she's kind of saying to herself, 'What am I doing here? Because I could go clean houses or hotels and make money,'" said Dudley.</p>

    <p>It's also not always a welcoming environment for these immigrants, according to Dudley and Mora. In school where there are very few students learning to speak English, Mora says she's often seen students be misunderstood, and she says making sure every student's potential is seen would be the most transformative change for schools in the state.</p>

    <p>"They're not an empty vessel. We think that 'Oh, my God, they know nothing.' And so that's the sad part," said Mora. "Could we start with what they actually can do as opposed to what they can't?"</p>
  </div>

  <div class="method-section">
    <h3 class="method-heading">Methodological Notes</h3>
    <dl class="method-list">

      <div class="method-item">
        <dt>Rural classification</dt>
        <dd>NCES Urban-Centric Locale Codes 41/42/43 (2023-24), assigned at the district level by the NCES EDGE program. For the purposes of clarity the subcategories are consolidated under the umbrella term.</dd>
        <div class="locale-tabs">
          {#each ALL_LOCALES as locale}
            <button
              class="locale-tab"
              class:active={activeLocaleTab === locale}
              onclick={() => activeLocaleTab = locale}
            >{locale}</button>
          {/each}
        </div>
        <div class="locale-panel">
          {#each LOCALE_DEFS[activeLocaleTab] as sub, i}
            {#if i > 0}<div class="sub-divider"></div>{/if}
            <div class="locale-sub">
              <span class="sub-name">{sub.name}</span>
              <span class="sub-desc">{sub.desc}</span>
            </div>
          {/each}
        </div>
        <p class="locale-source">Source: <a href="https://nces.ed.gov/programs/edge/Geographic/LocaleBoundaries" target="_blank" rel="noopener">NCES Locale Classifications</a></p>
      </div>

      <div class="method-item">
        <dt>Cohort</dt>
        <dd>2020 NYS 4-year cohort, outcome measured August 2024.</dd>
      </div>

      <div class="method-item">
        <dt>Suppressed values</dt>
        <dd>Districts below NYS reporting threshold are excluded from rate calculations (treated as missing, not zero).</dd>
      </div>

      <div class="method-item">
        <dt>Unmatched districts</dt>
        <dd>6 NYC charter schools could not be matched to NCES IDs and are excluded.</dd>
      </div>

      <div class="method-item">
        <dt>Data sources</dt>
        <dd>NYS Education Department 2023-24 ELL files; NCES CCD LEA Directory 2024-25; NCES EDGE Geocode LEA 2023-24. NYSED data files provided information on home languages, enrollment and graduation rates for ELL students in specific school districts. NCES EDGE provides the classifications of rural, town, suburban and urban and the NCES was simply used to provide unique IDs that allowed the classifications to be linked to the schools on the NYSED data.</dd>
      </div>

    </dl>
  </div>
</div>

<style>
  .article-body {
    margin-top: 40px;
    padding-top: 24px;
    border-top: 1px solid #e0e0e0;
  }

  .article-body p {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 17px;
    line-height: 1.75;
    color: #222;
    margin-bottom: 20px;
  }

  .article-body iframe {
    margin: 28px 0;
  }

  .map-subheadline {
    font-family: sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #111;
    margin: 24px 0 10px;
    line-height: 1.2;
  }

  .article-kicker {
    font-family: sans-serif;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #3370B8;
    margin-bottom: 8px;
  }

  .share-bar {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 10px 0 0;
    padding-bottom: 14px;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 24px;
  }

  .share-link {
    display: flex;
    align-items: center;
    opacity: 0.85;
    transition: opacity 0.15s;
    text-decoration: none;
  }

  .share-link:hover {
    opacity: 1;
  }

  .share-republish {
    margin-left: 4px;
    background: #ebebeb;
    color: #333;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 6px 14px;
    border-radius: 20px;
    transition: background 0.15s;
  }

  .share-republish:hover {
    background: #d8d8d8;
    color: #111;
  }

  .filter-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }

  .filter-label {
    font-family: sans-serif;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #555;
    margin-right: 4px;
  }

  .filter-btn {
    font-family: sans-serif;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 5px 14px;
    border: 1.5px solid #bbb;
    border-radius: 20px;
    background: #fff;
    color: #444;
    cursor: pointer;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
  }

  .filter-btn:hover {
    border-color: #258F6E;
    color: #258F6E;
  }

  .filter-btn.active {
    background: #258F6E;
    color: #fff;
    border-color: #258F6E;
  }

.school-count {
    margin-left: auto;
    background: #f5f5f5;
    border: 1.5px solid #ddd;
    border-radius: 6px;
    padding: 5px 12px;
    display: flex;
    align-items: baseline;
    gap: 5px;
  }

  .count-number {
    font-family: sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #258F6E;
  }

  .count-label {
    font-family: sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #666;
  }

  .stats-box {
    display: flex;
    align-items: center;
    gap: 20px;
    background: #f5f5f5;
    border: 1.5px solid #ddd;
    border-radius: 6px;
    padding: 12px 20px;
    margin-bottom: 12px;
    flex-wrap: wrap;
  }

  .stat {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 2px;
  }

  .stat-value {
    font-family: sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #111;
    line-height: 1;
  }

  .stat-label {
    font-family: sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #666;
  }

  .stat-divider {
    width: 1px;
    height: 36px;
    background: #ddd;
    flex-shrink: 0;
  }

  .stat-count {
    align-items: center;
  }

  .count-badge {
    font-family: sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #111;
    line-height: 1;
  }


  .map-wrapper {
    position: relative;
  }

  .missing-school-section {
    margin-top: 40px;
    padding-top: 24px;
    border-top: 2px solid #258F6E;
  }

  .db-search-wrapper {
    position: relative;
    margin-top: 14px;
    max-width: 500px;
  }

  .db-search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    color: #888;
    pointer-events: none;
  }

  .db-search {
    width: 100%;
    font-family: sans-serif;
    font-size: 15px;
    padding: 11px 14px 11px 38px;
    border: 1.5px solid #ccc;
    border-radius: 6px;
    outline: none;
    box-sizing: border-box;
    color: #222;
    background: #fff;
  }

  .db-search:focus {
    border-color: #258F6E;
  }

  .db-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1.5px solid #ccc;
    border-top: none;
    border-radius: 0 0 6px 6px;
    list-style: none;
    margin: 0;
    padding: 0;
    z-index: 20;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  }

  .db-result-btn {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 8px 12px;
    border: none;
    background: none;
    cursor: pointer;
    text-align: left;
    gap: 12px;
  }

  .db-result-btn:hover {
    background: #f5f5f5;
  }

  .db-result-name {
    font-family: sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #111;
  }

  .db-result-city {
    font-family: sans-serif;
    font-size: 12px;
    color: #888;
    white-space: nowrap;
  }

  .db-card-row-layout {
    display: flex;
    gap: 14px;
    margin-top: 12px;
    align-items: flex-start;
  }

  .db-card {
    flex: 1;
    min-width: 0;
    border: 1.5px solid #ddd;
    border-radius: 6px;
    padding: 14px 16px;
    background: #fafafa;
  }

  .db-mini-map {
    width: 180px;
    flex-shrink: 0;
    border-radius: 6px;
    overflow: hidden;
    border: 1.5px solid #ddd;
  }

  .db-mini-map :global(.map-figure) {
    margin: 0;
  }

  .db-mini-map :global(.maplibregl-ctrl-bottom-right) {
    display: none;
  }

  .db-card-name {
    font-family: sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #111;
    margin: 0 0 2px;
  }

  .db-card-location {
    font-family: sans-serif;
    font-size: 12px;
    color: #888;
    margin: 0 0 12px;
    text-transform: capitalize;
  }

  .db-card-stats {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .db-card-row {
    display: flex;
    gap: 8px;
    font-family: sans-serif;
    font-size: 13px;
    line-height: 1.4;
  }

  .db-card-row dt {
    font-weight: 700;
    color: #333;
    white-space: nowrap;
  }

  .db-card-row dd {
    color: #555;
    margin: 0;
  }

  .missing-school-headline {
    font-family: sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #3370B8;
    margin: 0 0 12px;
  }

  .missing-school-body {
    font-family: sans-serif;
    font-size: 15px;
    line-height: 1.7;
    color: #333;
    margin: 0 0 8px;
  }

  .missing-school-body:last-of-type {
    margin-bottom: 0;
  }

  .method-section {
    margin-top: 20px;
    padding: 12px 14px;
    background: #f9f9f9;
    border: 1px solid #e8e8e8;
    border-radius: 4px;
  }

  .method-heading {
    font-family: sans-serif;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #555;
    margin: 0 0 6px;
  }

  .method-list {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin: 0;
    padding: 0;
  }

  .method-item dt {
    display: inline;
    font-family: sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #333;
  }

  .method-item dd {
    display: inline;
    font-family: sans-serif;
    font-size: 12px;
    line-height: 1.5;
    color: #555;
    margin: 0;
  }

  .method-item dd::after {
    content: '';
    display: block;
    margin-bottom: 3px;
  }

  .locale-heading {
    font-family: sans-serif;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #555;
    margin: 0 0 10px;
  }

  .locale-tabs {
    display: flex;
    border-bottom: 2px solid #ddd;
    gap: 0;
    margin-bottom: 0;
    margin-top: 6px;
  }

  .locale-tab {
    font-family: sans-serif;
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border: none;
    background: none;
    color: #666;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: color 0.15s, border-color 0.15s;
  }

  .locale-tab:hover {
    color: #258F6E;
  }

  .locale-tab.active {
    color: #258F6E;
    border-bottom-color: #258F6E;
    font-weight: 700;
  }

  .locale-panel {
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 6px 6px;
    background: #fafafa;
  }

  .locale-sub {
    display: flex;
    flex-direction: column;
    padding: 8px 12px;
  }

  .sub-divider {
    height: 1px;
    background: #e0e0e0;
    margin: 0 12px;
  }

  .sub-name {
    font-family: sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #222;
    margin-bottom: 2px;
  }

  .sub-desc {
    font-family: sans-serif;
    font-size: 13px;
    line-height: 1.4;
    color: #555;
  }

  .locale-source {
    font-family: sans-serif;
    font-size: 12px;
    color: #888;
    margin: 8px 0 0;
  }

  .locale-source a {
    color: #888;
  }

  .tooltip {
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 10px 13px;
    font-family: sans-serif;
    font-size: 13px;
    line-height: 1.7;
    pointer-events: none;
    z-index: 10;
    max-width: 260px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
  }

  .tt-label {
    font-weight: 700;
    color: #222;
  }

  .tooltip.is-pinned {
    pointer-events: auto;
  }

  .tooltip-close {
    float: right;
    background: none;
    border: none;
    font-size: 12px;
    color: #999;
    cursor: pointer;
    padding: 0 0 2px 6px;
    line-height: 1;
  }

  .tooltip-close:hover {
    color: #333;
  }
</style>
