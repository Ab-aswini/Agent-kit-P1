# Submission & Verification Checklist

## Google Search Console (GSC)

```
Step 1: Add Property
  → Go to: search.google.com/search-console
  → Click "Add Property"
  → Choose "Domain" property (covers www + non-www + http + https)
  → Copy the TXT record → Add to DNS at your registrar
  → Wait 15-60 min → Click "Verify"

Step 2: Submit Sitemap
  → Left sidebar → Sitemaps
  → Enter: sitemap_index.xml
  → Click Submit
  → Status should show "Success" within 24-48 hours

Step 3: Configure Settings
  → Settings → International Targeting → Set target country
  → Settings → Email preferences → Enable ALL alert types

Step 4: Link Google Analytics 4
  → Settings → Associations → Google Analytics
  → Select your GA4 property → Link

Step 5: Initial Audit (after 48 hours)
  → Coverage → Check all Errors → Fix before Warnings
  → Core Web Vitals → Both Mobile and Desktop must be "Good"
  → URL Inspection → Test top 10 pages individually

Step 6: Request Indexing (New Site)
  → URL Inspection → enter URL → "Request Indexing"
  → Do this for: Homepage, all service/product pages, top blog posts
```

---

## Bing Webmaster Tools

```
Step 1: Add Site
  → Go to: bing.com/webmasters
  → Sign in with Microsoft account
  → Add Site → Enter domain → Verify

Step 2: Import from GSC (Fastest Method)
  → "Import from Google Search Console" option
  → Authorize → Select GSC property → Import
  → This imports: sitemap, verification, settings

Step 3: Submit Sitemap (if not imported)
  → Sitemaps → Submit sitemap
  → Enter: https://DOMAIN/sitemap_index.xml

Step 4: Enable IndexNow
  → Create key file at: https://DOMAIN/YOURKEY.txt
  → File contents: just the key string, nothing else
  → Verify key in Bing dashboard
  → Now submit URLs instantly via API (see technical-seo.md §indexnow)
```

---

## Google Business Profile (GBP)

```
Step 1: Claim/Create
  → Go to: business.google.com
  → Search your business name → Claim OR Create new

Step 2: Verify
  → Best: Phone/Email verification (instant)
  → Fallback: Postcard (5-14 days by mail)
  → Enter PIN when received

Step 3: Complete Profile (100% completion required)
  □ Business name (exact match to schema + website)
  □ Primary category (be specific — not just "Business")
  □ Additional categories (up to 9)
  □ Phone number (match schema exactly)
  □ Website URL
  □ Complete address (match schema exactly)
  □ Business hours
  □ Description (750 chars — include primary keyword naturally)
  □ Products/Services (add each with description + price)
  □ Attributes (women-led, online appointments, etc.)

Step 4: Photos
  Upload minimum 10 photos:
  - Exterior (from street)
  - Interior
  - Products/work samples
  - Team photos
  - Logo (square format)
  - Cover photo (1080×608px)

Step 5: NAP Consistency Check
  Name, Address, Phone must be IDENTICAL across:
  □ GBP listing
  □ Website footer + contact page
  □ Organization schema markup
  □ LocalBusiness schema markup
  □ All directory listings (JustDial, IndiaMart, Sulekha, etc.)

Step 6: Q&A Pre-Population
  → Go to your GBP → Q&A section
  → Ask your own FAQs (as a user) → Answer them (as owner)
  → Match these to your FAQ schema on the website

Step 7: Ongoing (Weekly)
  → Post Google Posts (offers, updates, events)
  → Respond to ALL reviews within 24 hours
  → Update photos monthly
  → Add new products/services as they launch
```

---

## Post-Launch Validation Commands

```bash
# Open all validation tools at once (copy-paste into terminal)

# 1. Google Rich Results Test
open "https://search.google.com/test/rich-results?url=https://YOURDOMAIN.com"

# 2. Google PageSpeed (Mobile)
open "https://pagespeed.web.dev/?url=https://YOURDOMAIN.com&strategy=mobile"

# 3. Open Graph Debugger
open "https://developers.facebook.com/tools/debug/?q=https://YOURDOMAIN.com"

# 4. Twitter Card Validator
open "https://cards-dev.twitter.com/validator"

# 5. Schema Markup Validator
open "https://validator.schema.org/?url=https://YOURDOMAIN.com"

# 6. Google Mobile Friendly Test
open "https://search.google.com/test/mobile-friendly?url=https://YOURDOMAIN.com"

# 7. Check robots.txt parsing
open "https://search.google.com/search-console/robots-testing-tool?url=https://YOURDOMAIN.com"

# 8. Ping sitemap to Google
curl "https://www.google.com/ping?sitemap=https://YOURDOMAIN.com/sitemap_index.xml"

# 9. Check indexation (paste in browser)
# site:YOURDOMAIN.com
```

---

## Weekly Automation Tasks (n8n or cron)

```javascript
// Paste these URLs into n8n HTTP Request nodes

// 1. Ping sitemap (weekly)
GET https://www.google.com/ping?sitemap=https://DOMAIN/sitemap_index.xml

// 2. IndexNow batch submit (on publish)
POST https://api.indexnow.org/indexnow
Body: { host, key, keyLocation, urlList: [newlyPublishedUrls] }

// 3. GBP review check → alert if new review (daily)
// Use Google My Business API or SERPAPI

// 4. GSC Coverage check → alert on new errors (weekly)
// Use GSC API or email alerts from GSC settings
```

---

## Directory Submission (India-Specific)

For Indian businesses, also submit to:

```
□ JustDial: justdial.com/business
□ IndiaMart: seller.indiamart.com
□ Sulekha: sulekha.com/post-requirements
□ Quikr: quikr.com
□ TradeIndia: tradeindia.com
□ Shiksha (if education): shiksha.com
□ Practo (if healthcare): practo.com
□ MagicBricks (if real estate): magicbricks.com
□ 99acres (if real estate): 99acres.com
```

NAP must match exactly across ALL listings.
