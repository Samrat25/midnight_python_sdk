# Midnight SDK Frontend Setup

## Overview

A complete, production-ready frontend has been created for the Midnight SDK, mirroring the exact structure and design of the AlgoGate SDK frontend. The frontend features a modern, interactive landing page built with React, TypeScript, Vite, and Tailwind CSS.

## Project Structure

```
frontend/
├── public/
│   ├── favicon.svg          # Midnight-themed favicon
│   └── icons.svg            # SVG icon definitions
├── src/
│   ├── assets/              # Image assets (to be added)
│   ├── components/
│   │   ├── ui/
│   │   │   └── button.tsx   # Shadcn button component
│   │   ├── ShinyText.tsx    # Animated text effect
│   │   ├── ShinyText.css
│   │   ├── Silk.tsx         # 3D background shader
│   │   ├── SpotlightCard.tsx # Interactive card with spotlight
│   │   └── SpotlightCard.css
│   ├── lib/
│   │   └── utils.ts         # Utility functions (cn helper)
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # React entry point
│   └── index.css            # Global styles with Tailwind
├── .gitignore
├── components.json          # Shadcn configuration
├── eslint.config.js         # ESLint configuration
├── index.html               # HTML entry point
├── package.json             # Dependencies and scripts
├── README.md                # Project documentation
├── tsconfig.json            # TypeScript configuration
├── tsconfig.app.json        # App-specific TS config
├── tsconfig.node.json       # Node-specific TS config
└── vite.config.ts           # Vite configuration
```

## Key Features

### Design & UI
- **Privacy-first theme**: Purple/blue color scheme (#4a3aff primary)
- **Interactive components**: Spotlight cards with mouse-tracking effects
- **Animated text**: Shiny text effect for hero section
- **3D background**: WebGL shader-based animated background (Silk component)
- **Responsive design**: Mobile-first approach with Tailwind CSS

### Content Sections

1. **Hero Section**
   - Privacy-first blockchain development messaging
   - Zero-knowledge proof integration highlights
   - Compact language smart contracts
   - Python SDK integration

2. **Features Module**
   - Privacy by design
   - Secure smart contracts
   - Python SDK integration
   - Complete development flow

3. **Build Section**
   - 6-step guide from installation to monitoring
   - Code examples for:
     - SDK installation
     - Python quick start
     - Compact smart contract
     - State queries

### Technology Stack

- **React 19.2.4**: Latest React with concurrent features
- **TypeScript 5.9.3**: Type-safe development
- **Vite 8.0.1**: Fast build tool and dev server
- **Tailwind CSS 4.2.2**: Utility-first CSS framework
- **Motion (Framer Motion) 12.23.12**: Animation library
- **Three.js 0.167.1**: 3D graphics for background
- **Shadcn UI**: Component library with Base Nova style
- **Lucide React**: Icon library

## Installation & Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

Or with pnpm:
```bash
pnpm install
```

### 2. Development Server

```bash
npm run dev
```

The development server will start at `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

Output will be in the `dist/` folder.

### 4. Preview Production Build

```bash
npm run preview
```

## Customization Guide

### Colors
The color scheme is defined in `src/index.css`:
- Primary: `#4a3aff` (Midnight purple)
- Accent: `#7c5cff` (Light purple)
- Background: Dark theme with transparency

To change colors, update the CSS variables in the `:root` section.

### Content
All content is in `src/App.tsx`:
- `heroBullets`: Hero section bullet points
- `features`: Feature cards
- `guideSteps`: Build section steps
- `installCode`, `quickStartCode`, etc.: Code examples

### Links
Update the `resourceLinks` array in `App.tsx`:
- Documentation link
- GitHub repository link

## Components

### SpotlightCard
Interactive card with mouse-tracking spotlight effect.

```tsx
<SpotlightCard spotlightColor="rgba(74, 58, 255, 0.12)">
  Content here
</SpotlightCard>
```

### ShinyText
Animated text with gradient shine effect.

```tsx
<ShinyText
  text="Your text"
  color="#c9b3ff"
  shineColor="#ffffff"
  speed={2}
  direction="left"
/>
```

### Silk
3D animated background using WebGL shaders.

```tsx
<Silk
  speed={5}
  scale={1}
  color="#1a1a2e"
  noiseIntensity={1.4}
/>
```

## Next Steps

1. **Add Assets**: Place images in `src/assets/` folder
2. **Update Links**: Replace placeholder URLs with actual documentation and GitHub links
3. **Add Analytics**: Integrate analytics tracking if needed
4. **SEO**: Update meta tags in `index.html`
5. **Deploy**: Deploy to Vercel, Netlify, or your preferred hosting

## Differences from AlgoGate Frontend

The Midnight SDK frontend maintains the exact same structure and design patterns as AlgoGate, with these content adaptations:

1. **Color Scheme**: Changed from green (#137636) to purple (#4a3aff)
2. **Content**: Updated all text to reflect Midnight blockchain features
3. **Code Examples**: Python SDK examples instead of FastAPI
4. **Features**: Privacy-focused features instead of payment-focused
5. **Background**: Darker theme (#1a1a2e) for Midnight branding

## Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run lint`: Run ESLint
- `npm run preview`: Preview production build

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

## License

Same as the main Midnight SDK project.
