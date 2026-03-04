---
name: asset-architect
description: Frame-perfect visual asset workflows for website projects. Use when designing cinematic scroll animations, canvas-based sequences, AI video generation specs, or complete visual production pipelines for any business vertical.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Asset Architect V2.0 - Frame-Perfect Workflow Skill

> **Philosophy:** True cinematic storytelling through motion, not disconnected slides.
> **Core Principle:** START[N] + MOTION[N] + END[N] = START[N+1]

---

## 🎯 When to Use This Skill

Trigger when user requests:

- "Create complete asset workflow for [business type]"
- "Generate frame-perfect sequences for [website]"
- "Build cinematic scroll animation specifications for [vertical]"
- "I need image prompts and video sequences with exact continuity"
- "Design visual journey for [industry] website"
- Any mention of "canvas animation + scroll" + "seamless transitions"

---

## 🔧 Workflow Overview

```
PHASE 1: Sequence Design (Frame Specifications)
   ↓
PHASE 2: Color Consistency Matrix
   ↓
PHASE 3: AI Video Tool Specifications
   ↓
PHASE 4: Technical Implementation Blueprint
   ↓
PHASE 5: Pre-Production Checklist
   ↓
PHASE 6: Client Pitch Materials
```

---

## PHASE 1: FRAME-PERFECT SEQUENCE DESIGN

### Step 1: Define Visual Journey

**Question Set for User:**

1. What's the primary emotion/experience you want visitors to feel?
2. What's the logical spatial journey? (e.g., outside → inside → specific space)
3. How many key spaces/moments need to be shown? (3-5 recommended)
4. Any specific transitions that are important? (e.g., passing through door, ascending stairs)
5. Should sequences feel slow/luxurious or dynamic/energetic?

**Output: Sequence Map**

```
Sequence 1: [Start Point] → [End Point] (Duration: Xs)
Sequence 2: [Start Point] → [End Point] (Duration: Xs)
Sequence 3: [Start Point] → [End Point] (Duration: Xs)
```

### Step 2: Design START Frame

```markdown
### START FRAME (Frame 001)

SHOT TYPE: [Extreme Close-up / Close-up / Medium / Wide / Establishing]
Camera Position: [X meters distance, Y meters height, Z° angle]

Composition Breakdown:
- FOREGROUND (X% of frame):
  - Primary elements: [Specific objects, their appearance]
  - Colors: [Element]: #HEXCODE
  - Textures: [Describe materials, surfaces]
  - Focus state: [Sharp / Soft / Out of focus]
  
- MIDGROUND (Y% of frame):
  - Secondary elements: [Specific objects]
  - Focus state: [Sharp / Soft bokeh / Blurred]
  - Color palette: [Element]: #HEXCODE
  
- BACKGROUND (Z% of frame):
  - Context elements: [Environment, sky, walls]
  - Focus state: [Usually soft / out of focus]
  - Colors: [Element]: #HEXCODE

Technical Camera Settings:
- Focal Length: [Xmm equivalent]
- Aperture: f/X.X
- Focus Point: [Specific element at X distance]
- Depth of Field: [Xm before to Ym after]

Lighting Specification:
- Time of Day: [Morning / Midday / Golden Hour / Evening]
- Primary Light Source: [Sun / Window / Artificial]
- Light Direction: [Front-lit / Side-lit / Back-lit / Top-down]
- Light Quality: [Hard / Soft]
- Color Temperature: [X Kelvin]

Color Verification:
✓ Brand Primary (#HEXCODE) visible in [element]
✓ Brand Accent (#HEXCODE) visible in [element]
✓ Neutral Background (#HEXCODE) established
```

### Step 3: Design Motion (Frame-by-Frame)

```markdown
### MOTION DESCRIPTION (Frames 001-XXX)

Camera Movement Type:
- Primary: [Crane up/down, Dolly forward/back, Truck left/right, Orbit]
- Movement Quality: [Smooth linear / Ease-in / Ease-out / Ease-in-out]

Frame-by-Frame Transformation Logic:

**Frames 001-030 (0-1 second):**
- [Primary element] occupies [X%] of frame
- Camera at [position description]
- Focus on [element at distance X]
- [What's changing this second]

**Frames 031-060 (1-2 seconds):**
- [Continuation from previous]
- New elements entering: [description]
- Elements exiting: [description]
- Focus shift: [from where to where]

[Continue for complete sequence duration]
```

### Step 4: Design END Frame

Same detailed format as START frame, with continuity checks:

```
CRITICAL: Verify END frame can serve as START frame for next sequence.
- Camera position achievable from next starting position ✓
- Lighting consistent with next sequence ✓
- Composition provides logical continuation ✓
- Color palette maintained ✓
```

### Step 5: Continuity Verification

```
END Frame Camera Position: [8m distance, 1.6m height, 0° angle]
NEXT Sequence START Position: [8m distance, 1.6m height, 0° angle] ✓ MATCH
Lighting Transition: [None / Gradual interior→exterior]
Color Consistency: [List hex codes present in both frames]
```

---

## PHASE 2: COLOR CONSISTENCY MATRIX

| Element | Hex Code | RGB | Where Used | Consistency Rule | Variation Allowed |
|---------|----------|-----|------------|------------------|--------------------|
| Brand Primary | #XXXXXX | R,G,B | [Locations] | Exact match required | Brightness ±5% max |
| Brand Accent | #XXXXXX | R,G,B | [Locations] | Exact match required | None |
| Background | #XXXXXX | R,G,B | [Locations] | Hue consistent | Brightness ±15% |
| Text/Dark | #XXXXXX | R,G,B | [Locations] | High contrast (4.5:1 min) | None |

**Lighting Temperature Map:**

| Space Type | Color Temperature | Kelvin | Hex Approximation |
|------------|-------------------|--------|--------------------|
| Exterior Daylight | Neutral/Cool | 5500K | #FFFFFA |
| Interior Warm | Warm White | 3000-4000K | #FFF4E6 |
| Interior Neutral | Neutral White | 4000-5000K | #FFFEF0 |
| Golden Hour | Warm Golden | 3000-3500K | #FFE4B5 |

---

## PHASE 3: AI VIDEO TOOL SPECIFICATIONS

### Tool Selection Matrix

| Tool | Best For | Max Duration | Motion Control | Cost |
|------|----------|-------------|----------------|------|
| Runway Gen-3 Alpha | Photorealistic, precise camera | 10s | Excellent | High ($12+/s) |
| Pika Labs | Fast turnaround, decent quality | 4s | Good | Medium ($1/s) |
| Stable Video Diffusion | Open source, batch processing | Flexible | Moderate | Free (compute) |
| Leonardo Motion | Illustrated/stylized | 4s | Low | Low ($0.30/frame) |

### Runway Gen-3 Prompt Format

```
Sequence [N]: [Title]

Camera Motion: [Detailed movement description]
Starting Frame: [Upload image_start_N.jpg]
Ending Frame: [Upload image_end_N.jpg]
Duration: [X] seconds
Style: Photorealistic, cinematic, [vertical-specific style]
Avoid: text, watermarks, people, morphing, warping, sudden jumps

Advanced Settings:
- Motion Consistency: Maximum
- Temporal Coherence: High
- Camera Motion: [Dolly / Crane / Orbit / Pan / Tilt]
- Motion Strength: [5-7 for architectural]
```

### Pika Labs Prompt Format

```
[Comprehensive scene description]
Starting frame: [Detailed start composition, camera position, lighting]
Ending frame: [Detailed end composition, camera position, lighting]
Camera motion: [Movement type] [direction and path]
Style: photorealistic architectural photography
-neg: text, watermarks, logos, people, morphing
```

### Stable Video Diffusion Config

```yaml
model: stabilityai/stable-video-diffusion-img2vid-xt
inputs:
  image: sequence_N_start.jpg
  prompt: [Detailed scene description]
  negative_prompt: text, watermarks, morphing, distortion
parameters:
  num_frames: [75-180 based on duration]
  fps: 30
  motion_bucket_id: [75-100 for architectural]
  noise_aug_strength: 0.02
output:
  format: "frames"
  naming: "%04d.jpg"
```

### Universal Export Settings

- **Canvas Animation:** JPEG sequence, 85-90% quality, 4-digit zero-padded
- **HTML5 Video:** MP4 H.264, 5-8 Mbps (1080p), WebM VP9 fallback
- **Resolution:** 1920x1080 minimum, 3840x2160 preferred
- **Frame Rate:** 30fps web standard, 60fps premium

---

## PHASE 4: TECHNICAL IMPLEMENTATION BLUEPRINT

### Canvas Sequence Manager Component

```typescript
// components/animations/SequenceManager.tsx
import { useEffect, useState, useRef, useCallback } from 'react';

interface Sequence {
  id: string;
  path: string;
  frameCount: number;
}

export default function SequenceManager({ sequences, containerHeight }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [allFrames, setAllFrames] = useState(new Map());
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);

  const totalFrames = sequences.reduce((sum, seq) => sum + seq.frameCount, 0);

  // Preload all sequences
  useEffect(() => {
    const loadAllSequences = async () => {
      const frameMap = new Map();
      let loadedTotal = 0;

      for (const sequence of sequences) {
        const frames = [];
        for (let i = 1; i <= sequence.frameCount; i++) {
          const img = new Image();
          img.src = `${sequence.path}/${String(i).padStart(4, '0')}.jpg`;
          await img.decode();
          frames.push(img);
          loadedTotal++;
          setProgress(Math.round((loadedTotal / totalFrames) * 100));
        }
        frameMap.set(sequence.id, frames);
      }
      setAllFrames(frameMap);
      setLoading(false);
    };
    loadAllSequences();
  }, [sequences, totalFrames]);

  // Scroll-driven frame rendering
  const renderCurrentFrame = useCallback((scrollProgress) => {
    const canvas = canvasRef.current;
    if (!canvas || allFrames.size === 0) return;
    const context = canvas.getContext('2d');
    if (!context) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    context.scale(dpr, dpr);

    const currentFrame = Math.floor(scrollProgress * totalFrames);
    let frameCount = 0;
    for (const sequence of sequences) {
      const sequenceStart = frameCount;
      if (currentFrame >= sequenceStart && currentFrame < sequenceStart + sequence.frameCount) {
        const sequenceFrames = allFrames.get(sequence.id);
        if (sequenceFrames) {
          const frame = sequenceFrames[currentFrame - sequenceStart];
          if (frame?.complete) {
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(frame, 0, 0, rect.width, rect.height);
          }
        }
        break;
      }
      frameCount += sequence.frameCount;
    }
  }, [allFrames, sequences, totalFrames]);

  useEffect(() => {
    if (loading) return;
    const handleScroll = () => {
      const container = containerRef.current;
      if (!container) return;
      const rect = container.getBoundingClientRect();
      const scrollProgress = Math.max(0, Math.min(1, -rect.top / (rect.height - window.innerHeight)));
      renderCurrentFrame(scrollProgress);
    };
    window.addEventListener('scroll', handleScroll);
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [loading, renderCurrentFrame]);

  if (loading) {
    return (
      <div className="loading-container">
        <div>Loading Sequences... {progress}%</div>
        <div className="progress-bar" style={{ width: `${progress}%` }} />
      </div>
    );
  }

  return (
    <div ref={containerRef} style={{ height: containerHeight, position: 'relative' }}>
      <div style={{ position: 'sticky', top: 0, height: '100vh' }}>
        <canvas ref={canvasRef} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
    </div>
  );
}
```

---

## PHASE 5: PRE-PRODUCTION CHECKLIST

### Sequence Design

- [ ] All sequences have START frames fully specified
- [ ] All sequences have END frames fully specified
- [ ] Frame-by-frame motion breakdown completed
- [ ] START[N+1] matches END[N] for all adjacent sequences
- [ ] Camera positions physically achievable
- [ ] Total duration appropriate for web (15-25s recommended)

### Color Consistency

- [ ] Color consistency matrix generated with hex codes
- [ ] Brand colors used consistently across all sequences
- [ ] Lighting temperature mapped for each space
- [ ] Contrast ratios verified for text overlays (4.5:1 min)

### Frame & Video Generation

- [ ] START/END frame images generated and verified
- [ ] AI tool prompts prepared (tool-specific format)
- [ ] Color picker verification completed
- [ ] JPEG sequences exported (0001.jpg format, no gaps)

### Technical Implementation

- [ ] Canvas component built with scroll-driven rendering
- [ ] DPR-aware sizing (Retina display support)
- [ ] Performance tested (60fps maintained)
- [ ] Mobile frame counts reduced (60-90 instead of 120-180)
- [ ] Loading states designed and implemented

### Deployment

- [ ] Cross-browser tested (Chrome, Safari, Firefox, Edge)
- [ ] Core Web Vitals checked (LCP<2.5s, CLS<0.1, INP<200ms)
- [ ] Production deployment completed
- [ ] Analytics configured

---

## Vertical-Specific Examples

### Luxury Hotel

- **Flow:** Texture → Exterior → Entrance → Suite → View
- **Palette:** #F5F5F5 (warm white), #C9A977 (gold), #2C2C2C (charcoal)
- **Tempo:** 1.2-1.5s (slow, elegant)
- **Durations:** 5-6s per sequence, 150-180 frames each

### Business Hotel

- **Flow:** Glass Detail → Building → Reception → Room → Amenities
- **Palette:** #1E88E5 (blue), #00ACC1 (cyan), #F5F5F5 (gray), #212121 (dark)
- **Tempo:** 0.6-0.8s (efficient)
- **Durations:** 4-5s per sequence, 120-150 frames each

### Fine Dining Restaurant

- **Flow:** Ingredients → Facade → Dining Room → Kitchen → Plated Dish
- **Palette:** #1A1A1A (black), #FFD700 (gold), #FFFFFF (white)
- **Tempo:** 0.8-1s (sophisticated)
- **Durations:** 3-4s per sequence, 90-120 frames each

### Real Estate

- **Flow:** Aerial → Exterior → Entry → Living Spaces → View
- **Palette:** #FAF9F6 (warm white), #708090 (blue-gray), wood tones
- **Tempo:** 0.6-0.8s (comfortable)
- **Durations:** 4-5s per sequence, 120-150 frames each

---

## Anti-Patterns to Avoid

### ❌ Disconnected Shots

**Wrong:** Hotel exterior → Random room → Pool → Restaurant (no continuity)
**Right:** Exterior → Entrance → Lobby → Room (logical journey)

### ❌ Vague Motion

**Wrong:** "Camera moves smoothly from outside to inside"
**Right:** "Camera dollies forward from 8m to 3m, subject grows from 20% to 70% of frame over frames 1-90"

### ❌ Color Inconsistency

**Wrong:** Blue #1E88E5 → #2196F3 → #1976D2 across sequences
**Right:** Brand Blue #1E88E5 exactly in all sequences

### ❌ Impossible Camera Moves

**Wrong:** Ground level → suddenly aerial → back inside
**Right:** Ground → eye level crane up → logical entrance

### ❌ Lighting Jumps

**Wrong:** Bright exterior → suddenly dark interior
**Right:** Gradual dimming over frames 120-150 as entering

---

## Client Pitch Template

### ROI Calculation

```
Current: OTA bookings at 20-30% commission
Monthly OTA fees: ₹[X] × [Y bookings] × 25% = ₹[Z]
Annual savings with website: ₹[Z] × 12 = ₹[Total]
Website Investment: ₹[Cost]
Payback Period: ₹[Cost] / ₹[Z per month] = [N] months
```

### Pricing Tiers

- **Basic (₹35-40K):** 1-2 sequences, single page, WhatsApp booking
- **Standard (₹50-60K):** 3-4 sequences, multi-page, booking form, 6mo support
- **Premium (₹75-100K):** 5+ sequences, CMS, payments, 1yr maintenance

---

> **Remember:** Frame-perfect continuity is NON-NEGOTIABLE. Every sequence is a link in a cinematic chain — break one link and the entire experience falls apart.
