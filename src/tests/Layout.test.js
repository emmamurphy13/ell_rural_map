import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import SiteHeader from '$lib/components/Layout/SiteHeader.svelte';
import SiteFooter from '$lib/components/Layout/SiteFooter.svelte';

describe('SiteHeader', () => {
  it('renders the site title', () => {
    render(SiteHeader);
    expect(screen.getByLabelText('ELL Rural Map home')).toBeTruthy();
  });

  it('renders the search button', () => {
    render(SiteHeader);
    expect(screen.getByLabelText('Search')).toBeTruthy();
  });
});

describe('SiteFooter', () => {
  it('renders the site title', () => {
    render(SiteFooter);
    expect(screen.getByText('ELL Rural Map')).toBeTruthy();
  });

  it('renders footer navigation links', () => {
    render(SiteFooter);
    expect(screen.getByText('About')).toBeTruthy();
  });
});
