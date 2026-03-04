# Schema Markup Library (JSON-LD)

All schemas go inside `<script type="application/ld+json">` tags.
Validate at: <https://search.google.com/test/rich-results>

## Organization (Sitewide — every project)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Business Name]",
  "url": "https://DOMAIN",
  "logo": { "@type": "ImageObject", "url": "https://DOMAIN/logo.png", "width": 300, "height": 100 },
  "description": "[One sentence with primary keyword]",
  "foundingDate": "YYYY",
  "founder": { "@type": "Person", "name": "[Founder Name]" },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[PIN]",
    "addressCountry": "IN"
  },
  "contactPoint": { "@type": "ContactPoint", "telephone": "+91-XXXXXXXXXX", "contactType": "customer service" },
  "sameAs": ["https://linkedin.com/company/X", "https://twitter.com/X", "https://facebook.com/X"]
}
```

## WebSite + Sitelinks Searchbox (Homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "[Brand]",
  "url": "https://DOMAIN",
  "potentialAction": {
    "@type": "SearchAction",
    "target": { "@type": "EntryPoint", "urlTemplate": "https://DOMAIN/search?q={search_term_string}" },
    "query-input": "required name=search_term_string"
  }
}
```

## Article (Blog Posts)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Exact H1]",
  "description": "[Meta description]",
  "image": ["https://DOMAIN/image.jpg"],
  "author": { "@type": "Person", "name": "[Author]", "url": "https://DOMAIN/author/slug" },
  "publisher": { "@type": "Organization", "name": "[Brand]", "logo": { "@type": "ImageObject", "url": "https://DOMAIN/logo.png" } },
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://DOMAIN/POST-SLUG/" }
}
```

## FAQPage (AEO Critical — use on content-rich pages)

> **⚠️ Use only with genuine FAQs (5-10 real Q&As per page). Do NOT add empty or fabricated FAQs just for schema — Google may apply manual action penalties for FAQ spam.**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Exact question users type into Google/ChatGPT]",
      "acceptedAnswer": { "@type": "Answer", "text": "[Direct answer. First sentence answers completely. Under 300 words.]" }
    },
    {
      "@type": "Question",
      "name": "[Next question]",
      "acceptedAnswer": { "@type": "Answer", "text": "[Answer]" }
    }
  ]
}
```

## LocalBusiness (GBP Integration)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Name]",
  "image": "https://DOMAIN/storefront.jpg",
  "@id": "https://DOMAIN/#localbusiness",
  "url": "https://DOMAIN",
  "telephone": "+91-XXXXXXXXXX",
  "priceRange": "₹₹",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[PIN]",
    "addressCountry": "IN"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "[ACTUAL_LAT]", "longitude": "[ACTUAL_LNG]" },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00" }
  ]
}
```

> **⚠️ geo coordinates:** Always use real lat/lng from Google Maps. Never leave as 0.0/0.0.
> **⚠️ aggregateRating:** Only add `aggregateRating` when you have real reviews (`reviewCount` > 0). Google may flag pages with 0-review ratings as deceptive.

## BreadcrumbList (Every interior page)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://DOMAIN" },
    { "@type": "ListItem", "position": 2, "name": "[Category]", "item": "https://DOMAIN/category/" },
    { "@type": "ListItem", "position": 3, "name": "[Page]", "item": "https://DOMAIN/category/page/" }
  ]
}
```

## Product (E-commerce)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product Name]",
  "image": ["https://DOMAIN/product.jpg"],
  "description": "[Product description with primary keyword]",
  "sku": "[SKU]",
  "brand": { "@type": "Brand", "name": "[Brand Name]" },
  "offers": {
    "@type": "Offer",
    "url": "https://DOMAIN/product-slug/",
    "priceCurrency": "INR",
    "price": "[PRICE]",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  },
  }
}
```

> **⚠️ aggregateRating:** Only include when `reviewCount` > 0. Remove entirely for new products with no reviews.

## Service

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "[Service Name]",
  "description": "[Description with keyword]",
  "provider": { "@type": "Organization", "name": "[Brand]", "url": "https://DOMAIN" },
  "areaServed": { "@type": "Place", "name": "[City/Region]" },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "[Service Category]",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "[Sub-service]" } }
    ]
  }
}
```

## HowTo (Instructional content — AI engines love citing these)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[How to do X]",
  "description": "[What this guide covers]",
  "totalTime": "PT10M",
  "step": [
    { "@type": "HowToStep", "name": "[Step 1 Title]", "text": "[Step 1 instructions]", "position": 1 },
    { "@type": "HowToStep", "name": "[Step 2 Title]", "text": "[Step 2 instructions]", "position": 2 }
  ]
}
```

## Person (Author / Founder profiles)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "[Full Name]",
  "jobTitle": "[Title]",
  "url": "https://DOMAIN/about/",
  "image": "https://DOMAIN/author-photo.jpg",
  "description": "[Short bio with expertise keywords]",
  "sameAs": ["https://linkedin.com/in/X", "https://twitter.com/X"]
}
```

## Validation Commands

```bash
# Test structured data
open "https://search.google.com/test/rich-results?url=PAGE_URL"

# Test Open Graph
open "https://developers.facebook.com/tools/debug/?q=PAGE_URL"

# Test schema via API
curl "https://validator.schema.org/validate?url=PAGE_URL"

# Full page audit
open "https://pagespeed.web.dev/?url=PAGE_URL"
```
