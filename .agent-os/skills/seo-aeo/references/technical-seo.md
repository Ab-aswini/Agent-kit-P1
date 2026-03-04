# Technical SEO Reference

## §robots — robots.txt Template

```txt
User-agent: *
Disallow: /admin/
Disallow: /login/
Disallow: /checkout/
Disallow: /thank-you/
Disallow: /wp-admin/
Disallow: /?s=
Disallow: /tag/
Disallow: /page/
Allow: /wp-admin/admin-ajax.php

# AI Crawlers — Keep open for AEO citation eligibility
User-agent: GPTBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: https://DOMAIN/sitemap_index.xml
```

**Rules:**
- Never disallow /wp-content/ or /wp-includes/ — Google needs CSS/JS to render
- Never add Crawl-delay unless server is genuinely under load
- Always reference sitemap with full absolute URL
- Block thin/duplicate content paths: /tag/, /author/, /page/ (paginated), /?s= (search results)

---

## §sitemap — sitemap_index.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://DOMAIN/sitemap-pages.xml</loc>
    <lastmod>YYYY-MM-DD</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://DOMAIN/sitemap-posts.xml</loc>
    <lastmod>YYYY-MM-DD</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://DOMAIN/sitemap-products.xml</loc>
    <lastmod>YYYY-MM-DD</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://DOMAIN/sitemap-images.xml</loc>
    <lastmod>YYYY-MM-DD</lastmod>
  </sitemap>
</sitemapindex>
```

**URL Entry Rules:**
```xml
<url>
  <loc>https://DOMAIN/page-slug/</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.9</priority>
</url>
```

Priority scale:
- 1.0 → Homepage
- 0.9 → Key service/product pages
- 0.8 → Category pages
- 0.7 → Blog/article pages
- 0.5 → Misc static pages
- 0.3 → Tag/archive pages (only if indexable)

Never include:
- noindex pages
- paginated pages (page/2, page/3...)
- filtered/faceted URLs without canonical
- Thank-you, login, admin pages

---

## §meta — Full Head Block

```html
<!-- PRIMARY -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>[PRIMARY KW] | [BRAND] — [VALUE PROP ≤60 chars]</title>
<meta name="description" content="[KW in first 20 words. Max 155 chars. End with CTA.]">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="[Author or Brand]">
<link rel="canonical" href="https://DOMAIN/PAGE-SLUG/">

<!-- OPEN GRAPH -->
<meta property="og:type" content="[website|article|product|profile]">
<meta property="og:title" content="[Title]">
<meta property="og:description" content="[Hook-first, 2 sentences max]">
<meta property="og:image" content="https://DOMAIN/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="[Descriptive alt]">
<meta property="og:url" content="https://DOMAIN/PAGE-SLUG/">
<meta property="og:site_name" content="[Brand Name]">
<meta property="og:locale" content="en_IN">

<!-- TWITTER/X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@HANDLE">
<meta name="twitter:title" content="[Title]">
<meta name="twitter:description" content="[Description]">
<meta name="twitter:image" content="https://DOMAIN/twitter-card.jpg">
<meta name="twitter:image:alt" content="[Alt text]">

<!-- VERIFICATION -->
<meta name="google-site-verification" content="[GSC_TOKEN]">
<meta name="msvalidate.01" content="[BING_TOKEN]">

<!-- FAVICON -->
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#HEX">
```

OG Image spec: 1200×630px, <1MB, JPG or PNG

---

## §indexnow — Instant Indexing API

```javascript
// POST to submit new/updated URLs to Bing + Yandex instantly
const submitIndexNow = async (urls) => {
  const response = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      host: 'DOMAIN',
      key: 'YOUR_INDEXNOW_KEY',
      keyLocation: 'https://DOMAIN/YOUR_INDEXNOW_KEY.txt',
      urlList: urls
    })
  });
  return response.status; // 200 = success, 422 = invalid URLs
};

// Google Ping (legacy but still works)
// GET https://www.google.com/ping?sitemap=https://DOMAIN/sitemap_index.xml
```

Key file: Create a plain text file at `https://DOMAIN/YOUR_KEY.txt` containing only the key string.

---

## §cwv — Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP    | <2.5s | 2.5-4s | >4s |
| INP    | <200ms | 200-500ms | >500ms |
| CLS    | <0.1 | 0.1-0.25 | >0.25 |
| TTFB   | <800ms | 800-1800ms | >1800ms |
| FCP    | <1.8s | 1.8-3s | >3s |

Validation: `https://pagespeed.web.dev/?url=PAGE_URL`
