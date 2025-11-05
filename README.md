# Flood Risk Assessment Project Structure

This document provides a detailed overview of the project structure, configuration, and architecture for both frontend and backend components.

## Project Overview

```
flood-risk-assessment/
├── backend/
│   └── flood-analyser/
└── frontend/
    └── flood-analyser-frontend/
```

## Frontend Structure

### Directory Structure

```
frontend/flood-analyser-frontend/
├── app/                    # Next.js 13+ App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   └── ui/               # Shadcn UI components
│       ├── alert-dialog.tsx
│       ├── badge.tsx
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── label.tsx
│       ├── select.tsx
│       ├── separator.tsx
│       ├── tabs.tsx
│       └── textarea.tsx
├── lib/                   # Utility functions
│   └── utils.ts          # Helper utilities
├── public/               # Static assets
├── components.json       # Shadcn UI config
├── eslint.config.mjs     # ESLint configuration
├── next-env.d.ts        # Next.js TypeScript definitions
├── next.config.ts       # Next.js configuration
├── package.json         # Project dependencies
├── postcss.config.mjs   # PostCSS configuration
├── README.md           # Project documentation
├── start-dev.sh        # Development startup script
└── tsconfig.json       # TypeScript configuration
```

### Key Configuration Files

#### next.config.ts
```typescript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Additional Next.js configuration
}

export default nextConfig;
```

#### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

#### postcss.config.mjs
```javascript
module.exports = {
  plugins: {
    'tailwindcss': {},
    'autoprefixer': {},
  },
}
```

### Environment Variables (.env)
```plaintext
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_maps_api_key
```

## Backend Structure

### Directory Structure

```
backend/flood-analyser/
├── __init__.py           # Package initializer
├── main.py              # Main application logic
├── requirements.txt     # Python dependencies
├── runtime.txt         # Python version specification
├── start.py           # Application entry point
└── __pycache__/      # Python cache directory
```

### Key Configuration Files

#### requirements.txt
```plaintext
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
google-generativeai==0.3.0
python-multipart==0.0.6
pillow==10.1.0
pydantic==2.4.2
pydantic-settings==2.0.3
```

#### runtime.txt
```plaintext
python-3.9.0
```

#### Environment Variables (.env)
```plaintext
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8000
DEBUG=True
```

### API Structure

```python
# main.py structure
from fastapi import FastAPI

app = FastAPI(
    title="Flood Risk Assessment API",
    description="API for flood risk assessment using coordinate and image analysis",
    version="1.0.0"
)

# API Routes
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze/coordinates")
async def analyze_coordinates():
    # Coordinate analysis implementation

@app.post("/api/analyze/image")
async def analyze_image():
    # Image analysis implementation
```

## Development Setup

### Frontend Development
```bash
cd frontend/flood-analyser-frontend
npm install
npm run dev
```

### Backend Development
```bash
cd backend/flood-analyser
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python start.py
```

## Dependencies

### Frontend Dependencies
- Next.js 13+
- React 18+
- TypeScript 5+
- Tailwind CSS
- Shadcn/ui
- Google Maps JavaScript API

### Backend Dependencies
- FastAPI
- Uvicorn
- Google Generative AI (Gemini)
- Python 3.9+
- Pydantic
- Python-multipart
- Pillow

## Build and Deployment

### Frontend Build
```bash
npm run build
npm start  # for production server
```

### Backend Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Additional Configuration

### CORS Configuration (Backend)
```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### TypeScript Path Aliases (Frontend)
```json
// tsconfig.json paths
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"],
      "@components/*": ["./components/*"],
      "@lib/*": ["./lib/*"]
    }
  }
}
```

## Security Considerations

1. Environment Variables
   - All sensitive data stored in `.env` files
   - Different env files for development/production
   - Git-ignored sensitive files

2. API Security
   - Rate limiting implemented
   - CORS properly configured
   - Input validation using Pydantic models

3. Frontend Security
   - CSP headers configured
   - API keys properly handled
   - Type checking enabled

This structure provides a scalable, maintainable architecture for both frontend and backend components while following best practices for Next.js and FastAPI development.