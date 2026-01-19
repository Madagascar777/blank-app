# Changelog - BioRoots Daily Life Optimizer

## Version 2.2 - React/Next.js Implementation (2025-01-19)

### 🆕 New Implementation

#### React/Next.js Version
Complete rewrite in modern React/TypeScript stack alongside the existing Streamlit version.

**Why Two Versions?**
- **Streamlit**: Simple, Python-based, quick setup for personal use
- **React/Next.js**: Modern, interactive, production-ready for wider deployment

**Features:**
- ✅ Real-time biological tracking
- ✅ Intelligent meal analysis with instant feedback
- ✅ Preventive alert system
- ✅ Daily scoring with visual progress
- ✅ Responsive mobile-first design
- ✅ TypeScript for type safety
- ✅ Component-based architecture
- ✅ Modern UI with Tailwind CSS

**Tech Stack:**
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Lucide React icons
- Radix UI components

**Deployment Options:**
- Vercel (one-click)
- Netlify
- AWS Amplify
- Docker containers
- Any Node.js hosting

**Getting Started:**
```bash
cd react-app
npm install
npm run dev
```

See [react-app/README.md](react-app/README.md) for full documentation.

---

## Version 2.1 - Biological Meal Analysis (2025-01-19)

### ✨ Major New Features

#### 1. Advanced Meal Logging with Biological Analysis
- **Ingredient tracking** - Enter all ingredients for each meal
- **Calorie input** - Track caloric intake per meal
- **Quantity tracking** - Weight in grams
- **Real-time biological analysis** - Instant feedback on every meal

#### 2. Intelligent Biology Analysis Engine
The app now analyzes each meal and provides:

**🏆 Biology Level Rating**
- OPTIMAL (85-100): Excellent biological support
- GOOD (70-84): Positive biological impact  
- MODERATE (50-69): Some concerns
- POOR (0-49): Significant issues

**Analysis Categories:**

**Calorie Analysis**
- Optimal ranges for meals (400-600 kcal) vs snacks (<300 kcal)
- Warns about insufficient fuel or excessive portions
- Predicts insulin response and energy crashes

**Ingredient Intelligence**
- Detects high-GI carbs (white bread, rice, sugar, etc.)
- Identifies protein sources (chicken, fish, eggs, etc.)
- Recognizes healthy fats (avocado, nuts, olive oil, etc.)
- Warns about glucose spike risks

**Biological Impact Warnings**
- 🔴 **GLUCOSE SPIKE RISK**: Refined carbs without protein buffer
  - Explains: Insulin surge → Tryptophan → Serotonin/Melatonin → SLEEPINESS
- 🔴 **AFTERNOON SLUMP RISK**: Carb-heavy lunch during work hours
  - Explains: Post-lunch insulin + circadian dip = SEVERE DROWSINESS
- ⚠️ **BRAIN FOG**: Large portions diverting blood from brain
  - Explains: Blood to digestion → Reduced prefrontal cortex oxygen

**Timing-Based Analysis**
- **Breakfast**: Protein breakfast sets dopamine tone for the day
- **Lunch (12-2pm)**: Warns about carb-heavy meals during afternoon circadian dip
- **Dinner (8pm+)**: Approves evening carbs for sleep preparation
- **Snacks**: Different calorie thresholds and recommendations

**Personalized Recommendations**
- Suggests when to eat carbs vs protein
- Recommends protein sources to add
- Advises on meal timing optimization
- Provides glucose control strategies

#### 3. Enhanced Meal Display
- Expandable meal cards showing full analysis
- Progress bar for biological impact score (0-100)
- Color-coded problems (🔴) and benefits (✅)
- Actionable recommendations (💡)

### 🎨 UI Improvements
- Text area for ingredient input with helpful placeholder
- Split columns for quantity and calorie input
- Expandable meal history with detailed analysis
- Visual progress indicators for meal impact scores

### 🧬 Biological Science Integrated
The analysis engine incorporates:
- **Glycemic Index** principles
- **Insulin response** timing
- **Circadian rhythm** effects on digestion
- **Neurotransmitter** production requirements
- **Blood flow** distribution during digestion
- **Amino acid** availability for brain function

### Example Analysis Output

```
Lunch (13:00) - 500 kcal, 300g
Ingredients: white rice, chicken breast, vegetables

🏆 GOOD - Positive biological impact
Biological Impact Score: 75/100

✅ Biological Benefits:
- Contains protein - Supports neurotransmitter production
- Optimal calories (500 kcal) - Sustained energy without crash
- Protein-rich lunch - Maintains alertness through afternoon circadian dip

⚠️ Biological Problems:
- HIGH GLUCOSE SPIKE RISK - Contains refined carbs without adequate protein buffer
  → Biological effect: Rapid insulin surge → Tryptophan enters brain → 
    Serotonin/Melatonin production → SLEEPINESS

💡 Recommendations:
- GLUCOSE CONTROL: Pair carbs with protein/fat to slow absorption
- Consider brown rice or quinoa for lower glycemic response
```

---

## Version 2.0 - Enhanced Scoring & Manual Logging (2025-01-19)

### ✨ New Features

#### 1. Daily Scoring System
- **Real-time score calculation (0-100 points)**
  - Wake time consistency: 25 points
  - Sleep time consistency: 25 points
  - Meal tracking: 30 points
  - Meal quantity: 10 points
  - Movement frequency: 10 points

- **Grade system with visual feedback**
  - A+ (90%+): 🏆 Excellent
  - A (80-89%): ⭐ Great
  - B (70-79%): 👍 Good
  - C (60-69%): 📈 Improving
  - D (<60%): 💪 Keep Going

- **Score breakdown display**
  - See points earned in each category
  - Get personalized improvement suggestions
  - Track progress over time

#### 2. Manual Time Logging (GMT+3 Timezone)
- **Wake-up time logging**
  - Enter exact hour (0-23) and minute (0-59)
  - Based on GMT+3 timezone (Europe/Moscow)
  - Shows previously logged time
  - Scores based on consistency with target

- **Sleep time logging**
  - Manual bedtime entry
  - Track when you actually go to sleep
  - Compare against target bedtime
  - Consistency scoring

- **Enhanced meal logging**
  - **Quantity tracking in grams**
  - Meal type selection (Breakfast, Lunch, Dinner, Snack)
  - Composition tracking (Protein-heavy, Balanced, Carb-heavy)
  - Time-stamped entries
  - Display all logged meals for the day

#### 3. Real-time Clock Display
- Current time in GMT+3 timezone
- Date display with day of week
- Always visible at top of dashboard

### 🎨 UI Improvements
- New gradient score card with prominent display
- Color-coded score breakdown metrics
- Improved layout with 3-column manual logging section
- Today's meals displayed in organized list
- Enhanced visual hierarchy

### 🔧 Technical Changes
- Added `pytz` dependency for timezone support
- New scoring algorithm functions:
  - `calculate_daily_score()` - Computes daily score
  - `get_score_grade()` - Converts score to letter grade
  - `time_difference_minutes()` - Calculates time deviations
  - `get_current_time_gmt3()` - Gets current GMT+3 time

- Enhanced data structure:
  - Added `today_logs` with wake_time, sleep_time, meals array
  - Meal objects now include quantity, type, composition, time
  - Date tracking for daily logs

### 📝 Documentation Updates
- Updated README with scoring system explanation
- Added detailed workflow for manual logging
- Documented point distribution
- Added GMT+3 timezone information

---

## Version 1.0 - Initial Release

### Features
- Sleep quality & consistency tracking
- Blood glucose management (meal timing alerts)
- Cognitive load management (90-min work cycles)
- Movement & adenosine clearing
- Light exposure & circadian health
- Real-time biological alerts
- Custom schedule configuration
- Data persistence via JSON

### Core Principles
- Biology-based approach (not willpower)
- Preventive alerts before problems occur
- Educational content on biological mechanisms
- Mobile-responsive design
