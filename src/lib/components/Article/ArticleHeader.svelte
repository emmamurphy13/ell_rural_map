<!--
@component
ArticleHeader.svelte — NYCity News Service Style Article Header

Displays the headline and metadata line with icons in the NYCity style:
- Optional kicker (eyebrow label) above the headline
- Large serif headline (via Headline subcomponent)
- Bordered metadata box with date (via Pubdate) and authors (via Byline)

USAGE EXAMPLE:
<ArticleHeader
  headline="City Council Approves New Budget"
  kicker="City Hall"
  byline="Jane Smith, John Doe"
  pubDate="2024-01-15"
/>
-->
<script>
  import Kicker from './Kicker.svelte';
  import Headline from './Headline.svelte';
  import Byline from './Byline.svelte';
  import Pubdate from './Pubdate.svelte';

  let {
    headline, // Required: The main title of the article
    kicker = '', // Optional: Eyebrow label rendered above the headline
    byline = '', // Optional: The author's name(s)
    pubDate = '', // Optional: Publication date in YYYY-MM-DD format
  } = $props();
</script>

<header class="article-header">
  <Kicker text={kicker} />
  <Headline text={headline} />

  {#if byline || pubDate}
    <p class="meta-line">
      {#if byline}<span class="meta-by">By</span> <span class="meta-author">{byline}</span>{/if}
      {#if byline && pubDate}<span class="meta-sep"> | </span>{/if}
      {#if pubDate}<span class="meta-date">{pubDate}</span>{/if}
    </p>
  {/if}
</header>

<style lang="scss">
  @use '../../styles' as *;

  .article-header {
    margin-bottom: var(--spacing-md);
  }

  .meta-line {
    font-family: var(--font-sans);
    font-size: 14px;
    margin: 6px 0 0 0;
    color: #555;
    line-height: 1.4;
  }

  .meta-by {
    color: #555;
    font-weight: 400;
  }

  .meta-author {
    color: #111;
    font-weight: 700;
  }

  .meta-sep {
    color: #bbb;
    margin: 0 2px;
  }

  .meta-date {
    color: #555;
    font-weight: 400;
  }
</style>
