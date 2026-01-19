# 🧬 BioRoots - Daily Life Optimizer

A web-based dashboard that helps users improve daily life by addressing **9 biological root causes** of common issues like procrastination, fatigue, and cognitive exhaustion.

## Key Principle: Biology, Not Willpower

Most productivity advice relies on willpower and discipline. **This fails** because:

- Low glucose → impaired prefrontal cortex → no willpower available
- Sleep deprivation → adenosine accumulation → constant fatigue
- Neurotransmitter depletion → motivation collapse

**BioRoots instead** uses preventive alerts based on biological timers to work with your biology, not against it.

## Features

### Currently Implemented (MVP):

1. **Sleep Quality & Consistency Tracking**
   - Track sleep and wake times
   - Monitor consistency and circadian rhythm
   - Bedtime alerts to prevent irregular patterns

2. **Blood Glucose Management (Meal Timing)**
   - Real-time alerts when you haven't eaten in 3-4 hours
   - Meal logging with composition tracking
   - Preventive warnings BEFORE glucose crashes

3. **Cognitive Load Management**
   - 90-minute work cycle enforcement
   - Automatic break reminders
   - Prevents neurotransmitter depletion and decision fatigue

4. **Movement & Adenosine Clearing**
   - Movement tracking every 45-60 minutes
   - Alerts when sedentary too long
   - Helps clear adenosine and boost dopamine

5. **Light Exposure & Circadian Health**
   - Sunlight exposure logging
   - Outdoor time tracking
   - Morning light reminders for cortisol optimization

### Coming Soon (Expansion):

6. Difficulty Waking Up (morning cortisol optimization)
7. Focus-Breakthrough Sleep Impulse (intense focus detection)
8. Decision Fatigue Tracking (decision limit counter)
9. Irregular Work Schedule (consistency monitoring)

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

2. **Start Tracking**:
   - Click "Log Meal" after eating
   - Click "Start Work Session" when beginning focused work
   - Click "Log Movement" after walking/stretching
   - Click "Log Sunlight" after going outdoors

3. **Follow the Alerts**:
   - The dashboard shows real-time biological condition alerts
   - 🔴 Red alerts = critical (take action immediately)
   - 🟡 Yellow alerts = warning (plan to act soon)
   - 🟢 Green status = optimal

### Daily Workflow:

1. **Morning**: Log wake time, get sunlight exposure
2. **Throughout Day**: 
   - Log meals every 3-4 hours
   - Start/stop work sessions (90-min cycles)
   - Log movement every 45-60 minutes
3. **Evening**: Follow bedtime alert to maintain consistency

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

- **Framework**: Streamlit (Python)
- **Data Storage**: JSON file (user_data.json)
- **State Management**: Streamlit session state
- **Responsive**: Mobile-friendly UI with custom CSS

## Data Persistence

The app stores your data in `user_data.json` including:
- Your biological schedule (sleep, meal, work times)
- Daily activity logs
- Current session tracking

This data persists across sessions so you can track patterns over time.

## License

MIT License - See LICENSE file for details
