<script>
  import { base } from '$app/paths';
  const currentYear = new Date().getFullYear();
</script>

<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-summary">
      <a href="{base}/" class="footer-home">ELL Rural Map</a>
      <p class="footer-description">
        Interactive reporting on English Language Learner graduation outcomes in rural New York.
      </p>
    </div>

    <nav class="footer-links" aria-label="Footer navigation">
      <a href="{base}/" class="footer-link">Home</a>
      <a href="{base}/map" class="footer-link">Map</a>
      <a href="{base}/data" class="footer-link">Data</a>
      <a href="{base}/about" class="footer-link">About</a>
    </nav>

    <p class="footer-copyright">&copy;{currentYear} ELL Rural Map</p>
  </div>
</footer>

<style>
  .site-footer {
    background: #f5f0e4;
    color: #111111;
    margin-top: 60px;
    font-family: Georgia, 'Times New Roman', serif;
  }

  .footer-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 48px 20px 32px;
  }

  .footer-summary {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 28px;
  }

  .footer-home {
    color: #0d2b1a;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 18px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .footer-home:hover {
    opacity: 0.85;
  }

  .footer-description {
    font-size: 15px;
    line-height: 1.5;
    margin: 0;
    max-width: 42rem;
  }

  .footer-links {
    display: flex;
    flex-wrap: wrap;
    gap: 14px 20px;
    margin-bottom: 22px;
  }

  .footer-link {
    color: #0d2b1a;
    text-decoration: none;
    font-family: sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .footer-link:hover {
    opacity: 0.8;
    text-decoration: underline;
  }

  .footer-copyright {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 13px;
    color: #555;
    margin: 0;
  }
</style>
