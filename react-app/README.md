# 🧬 BioRoots React Tracker

A modern React/Next.js implementation of the BioRoots Daily Life Optimizer with real-time biological tracking and meal analysis.

## Features

### Real-Time Tracking
- ⏰ **Sleep Tracking** - Log sleep and wake times with duration calculation
- 🍽️ **Meal Analysis** - Intelligent biological analysis of every meal
- 💼 **Work Sessions** - 90-minute cognitive load cycle tracking
- 🚶 **Movement** - Sedentary time tracking with adenosine clearing reminders
- ☀️ **Sunlight Exposure** - Circadian health optimization

### Intelligent Alerts
- **Preventive Alerts** - Warns BEFORE biological problems occur
- **Glucose Management** - Alerts when approaching 4-hour fasting threshold
- **Work Break Reminders** - Enforces 90-minute cognitive cycles
- **Movement Prompts** - Reminds to clear adenosine buildup
- **Sleep Consistency** - Tracks circadian rhythm disruptions

### Biological Meal Analysis
When you log a meal with ingredients, calories, and quantity, the app provides:

- **Biology Level Rating** (OPTIMAL/GOOD/MODERATE/POOR)
- **Impact Score** (0-100) 
- **Problem Detection**:
  - Glucose spike risks
  - Afternoon slump warnings
  - Brain fog alerts
  - Neurotransmitter concerns
- **Benefit Identification**:
  - Protein sources
  - Healthy fats
  - Optimal timing
- **Personalized Recommendations**:
  - What to add/change
  - Better timing suggestions
  - Ingredient swaps

### Daily Scoring
- Real-time score (0-100) based on:
  - Sleep consistency (40 points)
  - Meal tracking (30 points)
  - Meal quality (15 points)
  - Movement frequency (10 points)
  - Sunlight exposure (5 points)
- Letter grade (A+ to D)
- Visual progress tracking

## Technology Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **UI Components**: Radix UI primitives (via shadcn/ui)

## Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Setup

1. **Navigate to react-app directory**:
   ```bash
   cd react-app
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open in browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Usage

### Logging Sleep
1. Click "Go to Sleep" when you go to bed
2. Choose current time or enter manual time
3. Click "Wake Up" when you wake up
4. View sleep duration and consistency

### Logging Meals with Analysis
1. Click "Log & Analyze Meal"
2. Enter meal details:
   - Name (e.g., "Chicken Salad")
   - Ingredients (e.g., "chicken breast, lettuce, tomatoes, olive oil")
   - Calories (kcal)
   - Quantity (grams)
   - Meal type (Breakfast/Lunch/Dinner/Snack)
   - Composition (Protein-heavy/Balanced/Carb-heavy)
3. Set time (current or manual)
4. View instant biological analysis with:
   - Biology level rating
   - Impact score
   - Problems detected
   - Benefits identified
   - Personalized recommendations

### Tracking Work Sessions
1. Click "Start Work" when beginning focused work
2. App tracks duration and alerts at 85 and 90 minutes
3. Click "End Session" when taking break
4. View session history

### Logging Movement & Sunlight
1. Click "Log Movement" after physical activity
2. Click "Log Sunlight" after outdoor exposure
3. Track frequency and timing

## Biological Principles

### Meal Analysis Logic

The app analyzes meals based on:

**Ingredient Detection:**
- High-GI carbs: white bread, rice, pasta, sugar, soda
- Protein sources: chicken, beef, fish, eggs, tofu
- Healthy fats: avocado, nuts, olive oil, salmon

**Timing Analysis:**
- **Breakfast**: Protein sets dopamine tone for the day
- **Lunch (12-2pm)**: Carb-heavy meals risk afternoon slump
- **Dinner (8pm+)**: Carbs help sleep preparation
- **Snacks**: Different calorie thresholds

**Biological Impact:**
- Glucose spike risks from refined carbs without protein
- Afternoon slump from carb-heavy lunch + circadian dip
- Brain fog from large portions diverting blood from brain
- Neurotransmitter support from adequate protein

### Alert System

**Preventive Approach:**
- Alerts at 3.5 hours since last meal (before 4-hour critical threshold)
- Warning at 85 minutes of work (before 90-minute depletion)
- Movement reminder at 60 minutes sedentary

**Biology-Based:**
- Not based on arbitrary rules
- Grounded in circadian rhythm science
- Respects neurotransmitter cycles
- Optimizes glucose management

## Building for Production

```bash
npm run build
npm start
```

## Deployment

The app can be deployed to:
- **Vercel** (recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **Docker** containers
- Any Node.js hosting platform

### Vercel Deployment

1. Push code to GitHub
2. Import project in Vercel
3. Deploy with one click

## Comparison with Streamlit Version

| Feature | Streamlit | React/Next.js |
|---------|-----------|---------------|
| Setup | Simpler (pip install) | Requires Node.js ecosystem |
| UI | Server-rendered, simpler | More interactive, responsive |
| Customization | Limited | Highly customizable |
| Deployment | Streamlit Cloud, Heroku | Vercel, Netlify, AWS, etc. |
| Offline | Requires server | Can be PWA |
| Real-time | Page reloads | Live updates |
| Mobile | Basic responsive | Optimized responsive |

## Project Structure

```
react-app/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/
│   ├── BioRootsTracker.tsx # Main tracker component
│   └── ui/                 # UI components
│       ├── card.tsx
│       ├── button.tsx
│       └── alert.tsx
├── lib/
│   └── utils.ts            # Utility functions
├── public/                 # Static assets
├── package.json            # Dependencies
├── tailwind.config.ts      # Tailwind configuration
├── tsconfig.json           # TypeScript configuration
└── next.config.js          # Next.js configuration
```

## Development Roadmap

### Phase 1 (Current)
- ✅ Real-time biological tracking
- ✅ Intelligent meal analysis
- ✅ Alert system
- ✅ Daily scoring

### Phase 2 (Planned)
- 📊 Historical data visualization
- 📈 Pattern analysis and insights
- 🔔 Push notifications
- 💾 Local storage persistence
- 📱 Progressive Web App (PWA)

### Phase 3 (Future)
- 🔐 User authentication
- ☁️ Cloud sync
- 📊 Advanced analytics
- 🤝 Data export
- 🎯 Goal setting

## Contributing

This is part of the BioRoots project. For contributing guidelines, see the main project README.

## License

MIT License - See LICENSE file in root directory

## Support

For issues, questions, or feature requests, please refer to the main BioRoots project documentation.

## Key Differences from Original Implementation

This React version includes enhanced features:
- TypeScript for type safety
- Real-time meal analysis built into the UI
- More responsive and interactive interface
- Better mobile experience
- Component-based architecture for easier maintenance
- Modern UI with Tailwind CSS

## Credits

Built on biological principles from the BioRoots project.
Biology-based approach, not willpower-based.
