# Changelog - BioRoots Daily Life Optimizer

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
