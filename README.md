# 🧬 BioRoots - Daily Life Optimizer

A web-based dashboard that helps users improve daily life by addressing **9 biological root causes** of common issues like procrastination, fatigue, and cognitive exhaustion.

## 🚀 Two Implementations Available

**Choose the version that fits your needs:**

1. **Streamlit Version** (Python) - Simple, quick setup
   - Perfect for: Quick prototyping, Python developers, simple deployment
   - Run with: `streamlit run streamlit_app.py`
   - See below for setup instructions

2. **React/Next.js Version** (TypeScript) - Modern, interactive
   - Perfect for: Production apps, advanced features, better UX
   - Run with: `cd react-app && npm run dev`
   - See: [react-app/README.md](react-app/README.md)

## Key Principle: Biology, Not Willpower

Most productivity advice relies on willpower and discipline. **This fails** because:

- Low glucose → impaired prefrontal cortex → no willpower available
- Sleep deprivation → adenosine accumulation → constant fatigue
- Neurotransmitter depletion → motivation collapse

**BioRoots instead** uses preventive alerts based on biological timers to work with your biology, not against it.

## Features

### Currently Implemented (MVP):

1. **Intelligent Meal Analysis** 🆕 LATEST
   - **Enter ingredients, calories, and quantity for each meal**
   - **Real-time biological analysis** with impact scoring (0-100)
   - **Identifies problems**: Glucose spikes, afternoon slumps, brain fog
   - **Explains biology**: Why certain foods cause sleepiness or energy crashes
   - **Timing-based insights**: Different recommendations for breakfast/lunch/dinner
   - **Personalized tips**: What to add/change for better biological support
   - **Biology level grading**: OPTIMAL, GOOD, MODERATE, or POOR rating

2. **Daily Scoring System** ⭐
   - Real-time score (0-100) based on biological adherence
   - Grade system (A+ to D) with improvement suggestions
   - Score breakdown by category (sleep, meals, movement)
   - Tracks consistency with your biological schedule

3. **Manual Time Logging (GMT+3 Timezone)** ⭐
   - Log wake-up time with exact hour/minute
   - Log sleep time (bedtime) manually
   - Meal logging with ingredients, calories, and quantity
   - All times based on your local GMT+3 timezone

4. **Sleep Quality & Consistency Tracking**
   - Track sleep and wake times
   - Monitor consistency and circadian rhythm
   - Bedtime alerts to prevent irregular patterns
   - Score points for staying consistent with target times

5. **Blood Glucose Management (Meal Timing)**
   - Real-time alerts when you haven't eaten in 3-4 hours
   - Meal logging with full nutritional details
   - Preventive warnings BEFORE glucose crashes
   - Biological analysis explains insulin responses
   - Score points for eating 3+ meals per day with proper quantities

6. **Cognitive Load Management**
   - 90-minute work cycle enforcement
   - Automatic break reminders
   - Prevents neurotransmitter depletion and decision fatigue

7. **Movement & Adenosine Clearing**
   - Movement tracking every 45-60 minutes
   - Alerts when sedentary too long
   - Helps clear adenosine and boost dopamine
   - Score points for frequent movement

8. **Light Exposure & Circadian Health**
   - Sunlight exposure logging
   - Outdoor time tracking
   - Morning light reminders for cortisol optimization

### Coming Soon (Expansion):

8. Difficulty Waking Up (morning cortisol optimization)
9. Focus-Breakthrough Sleep Impulse (intense focus detection)
10. Decision Fatigue Tracking (decision limit counter)
11. Irregular Work Schedule (consistency monitoring)

## How to Run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the dashboard**
   - Open your browser to the URL shown (usually http://localhost:8501)

## How to Use

### First Time Setup:

1. **Configure Your Schedule** (in sidebar):
   - Set your target wake and sleep times
   - Set your meal times (breakfast, lunch, dinner)
   - Set your work hours
   - Times are in GMT+3 timezone

2. **Start Tracking - Manual Logging**:
   - **Wake-Up Time**: Enter hour and minute when you woke up today
   - **Sleep Time**: Enter hour and minute when you went to bed
   - **Meals**: Log each meal with ingredients, calories, quantity, and composition
   - **Movement**: Click "Log Movement" after walking/stretching
   - **Sunlight**: Click "Log Sunlight" after going outdoors

3. **Monitor Your Score**:
   - Your daily score (0-100) updates automatically
   - Get a grade from A+ to D based on adherence
   - See improvement suggestions tailored to your data
   - Track breakdown by category

4. **Follow the Alerts**:
   - The dashboard shows real-time biological condition alerts
   - 🔴 Red alerts = critical (take action immediately)
   - 🟡 Yellow alerts = warning (plan to act soon)
   - 🟢 Green status = optimal

### Daily Workflow:

1. **Morning**: 
   - Log your wake-up time (exact time you woke up)
   - Get sunlight exposure within 1 hour

2. **Throughout Day**: 
   - **Log meals with full details**:
     - Enter ingredients (comma-separated)
     - Input calories (kcal)
     - Specify quantity (grams)
     - Select composition (Protein-heavy/Balanced/Carb-heavy)
     - Get instant biological analysis
   - Review meal analysis for problems and recommendations
   - Start/stop work sessions (90-min cycles)
   - Log movement every 45-60 minutes

3. **Evening**: 
   - Log your sleep time when going to bed
   - Follow bedtime alert to maintain consistency
   - Check your daily score and improvement tips

### Biological Meal Analysis:

When you log a meal, the app provides intelligent analysis:

**What Gets Analyzed:**
- **Calories**: Optimal ranges differ for meals (400-600 kcal) vs snacks (<300 kcal)
- **Ingredients**: Detects high-GI carbs, protein sources, healthy fats
- **Timing**: Different recommendations for breakfast, lunch, dinner based on circadian rhythm
- **Quantity**: Warns about portions that may cause digestion issues or insufficient energy
- **Composition**: Analyzes protein/carb/fat balance

**Biology Level Ratings:**
- 🏆 **OPTIMAL (85-100)**: Excellent biological support
- ✅ **GOOD (70-84)**: Positive biological impact
- ⚠️ **MODERATE (50-69)**: Some biological concerns
- 🔴 **POOR (0-49)**: Significant biological issues

**Common Warnings:**
- **Glucose Spike Risk**: Refined carbs without protein → Insulin surge → Sleepiness
- **Afternoon Slump**: Carb-heavy lunch (12-2pm) → Post-lunch dip + circadian low = Severe drowsiness
- **Brain Fog**: Large portions → Blood diverted to digestion → Reduced brain oxygen
- **Low Protein**: Insufficient amino acids → Impaired neurotransmitter production

**Example:**
```
Input:
- Type: Lunch
- Ingredients: white rice, chicken breast, broccoli
- Calories: 500 kcal
- Quantity: 300g
- Time: 13:00

Analysis:
✅ Contains protein - Supports dopamine/norepinephrine production
✅ Optimal calories - Sustained energy without crash
⚠️ HIGH GLUCOSE SPIKE RISK - Refined carbs detected
💡 Recommendation: Switch to brown rice or add more protein

Biology Level: GOOD (75/100)
```

### Scoring System:

Your daily score is calculated from:
- **Wake Time (25 points)**: Consistency with target wake time
  - Within 15 min: 25 points
  - Within 30 min: 20 points
  - Within 60 min: 15 points
  
- **Sleep Time (25 points)**: Consistency with target bedtime
  - Within 15 min: 25 points
  - Within 30 min: 20 points
  - Within 60 min: 15 points

- **Meals (30 points)**: Number of meals logged
  - 3+ meals: 30 points
  - 2 meals: 20 points
  - 1 meal: 10 points

- **Meal Quantity (10 points)**: Total daily intake
  - 300-500g: 10 points
  - 200-600g: 7 points
  - Other: 3 points

- **Movement (10 points)**: Recent physical activity
  - Last hour: 10 points
  - Last 2 hours: 7 points
  - Longer: 3 points

## The 9 Biological Root Causes

### 1. PROCRASTINATION
**Root**: Poor sleep → impaired executive function | Low blood glucose → brain lacks fuel | Dopamine dysregulation  
**Solution**: Track sleep quality, enforce meal timing, detect fatigue buildup

### 2. DIFFICULTY WAKING UP
**Root**: High adenosine accumulation | Insufficient sleep → low morning cortisol | Inconsistent sleep schedule  
**Solution**: Sleep schedule tracker, bedtime enforcement, consistency monitoring

### 3. HUNGER → SLEEP CRASH
**Root**: Skipped meals → glucose drops | Eating carbs → insulin surge → melatonin → sleepiness  
**Solution**: Meal reminders BEFORE hunger, meal type guidance (protein-heavy during work)

### 4. COGNITIVE EXHAUSTION
**Root**: Sustained mental effort → glucose depletion → neurotransmitter drop (dopamine, acetylcholine)  
**Solution**: Mandatory 90-minute work cycles with breaks, light snacks during breaks

### 5. SLEEP IMPULSE DURING FOCUS
**Root**: Prolonged cognitive intensity → adenosine accumulates | High dopamine crash  
**Solution**: Movement break triggers, force pause during intense focus

### 6. IRREGULAR WORK SCHEDULE
**Root**: Inconsistent wake/sleep times → circadian rhythm disorder → unpredictable cortisol  
**Solution**: Set wake time consistency, meal time consistency, log schedule deviations

### 7. DECISION FATIGUE
**Root**: Daily decisions deplete prefrontal cortex glucose → ego depletion  
**Solution**: Decision limit tracker, decision-heavy vs decision-light time blocks

### 8. PROLONGED SITTING / NO MOVEMENT
**Root**: Sedentary work → blood glucose utilization drops | No movement → adenosine doesn't clear  
**Solution**: Movement break reminders every 30-45 min, track daily movement

### 9. INDOOR WORK / POOR LIGHT EXPOSURE
**Root**: No natural light → circadian rhythm desynchronizes | Low light → melatonin dysregulates  
**Solution**: Morning sunlight exposure reminder, outdoor time tracking

## Technical Details

- **Framework**: Streamlit (Python 3)
- **Dependencies**: streamlit, pandas, pytz
- **Timezone**: GMT+3 (Europe/Moscow timezone)
- **Data Storage**: JSON file (user_data.json)
- **State Management**: Streamlit session state
- **Scoring Algorithm**: Real-time calculation based on biological adherence
- **Responsive**: Mobile-friendly UI with custom CSS

## Data Persistence

The app stores your data in `user_data.json` including:
- Your biological schedule (sleep, meal, work times)
- Daily activity logs
- Current session tracking

This data persists across sessions so you can track patterns over time.

## License

MIT License - See LICENSE file for details
