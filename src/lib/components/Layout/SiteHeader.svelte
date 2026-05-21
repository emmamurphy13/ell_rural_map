<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';

  let scrolled = $state(false);

  onMount(() => {
    const sentinel = document.getElementById('scroll-sentinel');
    if (!sentinel) return;
    const observer = new IntersectionObserver(
      ([entry]) => { scrolled = !entry.isIntersecting; },
      { threshold: 0 }
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  });
</script>

<header class="site-header" class:scrolled>
  <!-- Top white bar: hidden when scrolled -->
  <div class="top-bar">
    <div class="top-bar-inner">
      <div class="top-bar-side top-bar-left"></div>

      <a href="https://www.chalkbeat.org/" class="logo-link" aria-label="Chalkbeat">
        <img src="{base}/chalkbeatlogo.png" alt="Chalkbeat" class="logo" />
      </a>

      <div class="top-bar-side top-bar-right">
        <a href="{base}/about" class="newsletters-btn">About</a>
      </div>
    </div>
  </div>

  <!-- Nav bar: gains branding when scrolled -->
  <div class="nav-bar">
    <nav class="nav-bar-inner" aria-label="Main navigation">

      <!-- Scrolled branding badges (only visible when scrolled) -->
      <div class="scroll-brand">
        <a href="https://www.chalkbeat.org/" class="brand-chalkbeat">Chalkbeat</a>
        <a href="https://www.chalkbeat.org/newyork/" class="brand-newyork">New York</a>
      </div>

      <a href="{base}/" class="nav-link">Home</a>

      <a href="{base}/map" class="nav-link">Map</a>

      <a href="{base}/data" class="nav-link">Data</a>

      <a href="{base}/about" class="nav-link">About</a>

      <!-- Search icon (always visible in nav, more prominent when scrolled) -->
      <button class="search-btn" aria-label="Search">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="7"/>
          <line x1="16.5" y1="16.5" x2="22" y2="22"/>
        </svg>
      </button>

    </nav>
  </div>
</header>

<style>
  .site-header {
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  /* ── Top white bar ── */
  .top-bar {
    background: #ffffff;
    border-bottom: 1px solid #e5e5e5;
    overflow: hidden;
    max-height: 200px;
    transition: max-height 0.3s ease, padding 0.3s ease, border-width 0.3s ease;
  }

  .scrolled .top-bar {
    max-height: 0;
    border-bottom-width: 0;
  }

  .top-bar-inner {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px 32px;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
  }

  .top-bar-side {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .top-bar-left {
    justify-content: flex-start;
  }

  .top-bar-right {
    justify-content: flex-end;
  }

  .logo-link {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .logo {
    height: 100px;
    width: auto;
    display: block;
  }

  .site-title {
    font-family: sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #0d2b1a;
    letter-spacing: 0.02em;
  }

  .newsletters-btn,
  .donate-btn {
    text-decoration: none;
    font-family: sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 11px 22px;
    border-radius: 0;
    transition: opacity 0.15s;
    display: inline-block;
  }

  .newsletters-btn {
    background: #aecad8;
    color: #0d2b1a;
  }

  .newsletters-btn:hover { opacity: 0.85; }

  .donate-btn {
    background: #0d2b1a;
    color: #ffffff;
  }

  .donate-btn:hover { opacity: 0.85; }

  /* ── Nav bar ── */
  .nav-bar {
    background: #aecad8;
  }

  .nav-bar-inner {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 32px;
    display: flex;
    align-items: stretch;
    flex-wrap: wrap;
    gap: 0;
  }

  /* ── Scrolled branding ── */
  .scroll-brand {
    display: none;
    align-items: stretch;
    margin-right: 8px;
  }

  .scrolled .scroll-brand {
    display: flex;
  }

  .brand-chalkbeat {
    background: #3666ec;
    color: #ffffff;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0 16px;
    display: flex;
    align-items: center;
  }

  .brand-newyork {
    background: #2e8070;
    color: #ffffff;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0 16px;
    display: flex;
    align-items: center;
  }

  .brand-site {
    background: #2e8070;
    color: #ffffff;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0 12px;
    display: flex;
    align-items: center;
  }

  .brand-chalkbeat:hover { opacity: 0.9; }
  .brand-newyork:hover { opacity: 0.9; }

  /* ── Nav links ── */
  .nav-link {
    color: #0d2b1a;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 14px 14px;
    white-space: nowrap;
    border-bottom: 3px solid transparent;
    transition: background 0.15s, border-color 0.15s;
  }

  .nav-link:hover {
    background: rgba(0,0,0,0.08);
    border-bottom-color: #0d2b1a;
  }

  /* ── Search button ── */
  .search-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #0d2b1a;
    display: flex;
    align-items: center;
    padding: 0 14px;
    margin-left: auto;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s;
  }

  .scrolled .search-btn {
    opacity: 1;
    pointer-events: auto;
  }

  .search-btn:hover {
    opacity: 0.7;
  }

  /* ── Dropdown nav items ── */
  .nav-item {
    position: relative;
    display: flex;
    align-items: stretch;
  }

  .nav-item .nav-link {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .chevron {
    opacity: 0.7;
    transition: transform 0.15s;
    flex-shrink: 0;
  }

  .nav-item:hover .chevron {
    transform: rotate(180deg);
  }

  .dropdown {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    min-width: 180px;
    background: #ffffff;
    border-top: 3px solid #0d2b1a;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    list-style: none;
    margin: 0;
    padding: 6px 0;
    z-index: 200;
  }

  .nav-item:hover .dropdown {
    display: block;
  }

  .dropdown-link {
    display: block;
    padding: 9px 18px;
    color: #1a1a1a;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
    transition: background 0.1s, color 0.1s;
  }

  .dropdown-link:hover {
    background: #e8f0ed;
    color: #0d2b1a;
  }
</style>
