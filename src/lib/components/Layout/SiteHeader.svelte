<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';

  let scrolled = $state(false);

  onMount(() => {
    const sentinel = document.getElementById('scroll-sentinel');
    if (!sentinel) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        scrolled = !entry.isIntersecting;
      },
      { threshold: 0 }
    );

    observer.observe(sentinel);
    return () => observer.disconnect();
  });
</script>

<header class="site-header" class:scrolled>
  <div class="top-bar">
    <div class="top-bar-inner">
      <div class="top-bar-side top-bar-left">
        <a href="{base}/" class="site-title-link" aria-label="ELL Rural Map home">
          ELL Rural Map
        </a>
      </div>

      <div class="top-bar-spacer"></div>

      <div class="top-bar-side top-bar-right">
        <a href="{base}/about" class="newsletters-btn">About</a>
      </div>
    </div>
  </div>

  <div class="nav-bar">
    <nav class="nav-bar-inner" aria-label="Main navigation">
      <a href="{base}/" class="nav-link">Home</a>
      <a href="{base}/map" class="nav-link">Map</a>
      <a href="{base}/data" class="nav-link">Data</a>
      <a href="{base}/about" class="nav-link">About</a>

      <button class="search-btn" aria-label="Search">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="7" />
          <line x1="16.5" y1="16.5" x2="22" y2="22" />
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
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

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

  .top-bar-spacer {
    min-height: 1px;
  }

  .site-title-link {
    color: #0d2b1a;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 10px 0;
  }

  .site-title-link:hover {
    opacity: 0.85;
  }

  .newsletters-btn {
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
    background: #aecad8;
    color: #0d2b1a;
  }

  .newsletters-btn:hover {
    opacity: 0.85;
  }

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
    background: rgba(0, 0, 0, 0.08);
    border-bottom-color: #0d2b1a;
  }

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

  @media (max-width: 640px) {
    .top-bar-inner {
      padding: 16px 20px;
      grid-template-columns: 1fr;
      gap: 12px;
      justify-items: center;
    }

    .top-bar-side {
      width: 100%;
      justify-content: center;
    }

    .top-bar-right {
      justify-content: center;
    }

    .nav-bar-inner {
      padding: 0 20px;
    }
  }
</style>
