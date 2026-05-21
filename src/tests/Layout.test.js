import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import SiteHeader from '$lib/components/Layout/SiteHeader.svelte';
import SiteFooter from '$lib/components/Layout/SiteFooter.svelte';

describe('SiteHeader', () => {
  it('renders the logo', () => {
    render(SiteHeader);
    expect(screen.getByLabelText('Chalkbeat')).toBeTruthy();
  });

  it('renders default navigation links', () => {
    render(SiteHeader);
    expect(screen.getByText('Home')).toBeTruthy();
  });

  it('renders the Map link', () => {
    render(SiteHeader);
    expect(screen.getByText('Map')).toBeTruthy();
  });

  it('renders the Data link', () => {
    render(SiteHeader);
    expect(screen.getByText('Data')).toBeTruthy();
  });
});

describe('SiteFooter', () => {
  it('renders the Chalkbeat logo', () => {
    render(SiteFooter);
    expect(screen.getByAltText('Chalkbeat')).toBeTruthy();
  });

  it('renders footer navigation links', () => {
    render(SiteFooter);
    expect(screen.getByText('About Us')).toBeTruthy();
  });
});
