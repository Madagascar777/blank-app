import streamlit as st
from datetime import datetime, time, timedelta, timezone
import pandas as pd
import json
from pathlib import Path
import pytz

# Page config
st.set_page_config(
    page_title="BioRoots - Daily Life Optimizer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E40AF;
        margin-bottom: 0.5rem;
    }
    .status-good {
        background-color: #D1FAE5;
        border-left: 4px solid #10B981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-warning {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-danger {
        background-color: #FEE2E2;
        border-left: 4px solid #EF4444;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #F9FAFB;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
        margin: 0.5rem 0;
    }
    .alert-box {
        background-color: #FEF2F2;
        border: 2px solid #DC2626;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .score-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence using session state and JSON
DATA_FILE = Path("user_data.json")

# GMT+3 timezone
GMT_PLUS_3 = pytz.timezone('Europe/Moscow')

def load_data():
    """Load user data from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'profile': {
            'target_wake_time': '07:00',
            'target_sleep_time': '23:00',
            'meal_times': ['08:00', '13:00', '19:00'],
            'work_start': '09:00',
            'work_end': '17:00',
            'timezone': 'GMT+3'
        },
        'daily_logs': [],
        'current_session': {},
        'today_logs': {
            'wake_time': None,
            'sleep_time': None,
            'meals': [],
            'date': None
        }
    }

def save_data(data):
    """Save user data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def get_current_time_gmt3():
    """Get current time in GMT+3"""
    return datetime.now(GMT_PLUS_3)

def time_difference_minutes(target_time_str, actual_time_str):
    """Calculate difference in minutes between two times"""
    target = datetime.strptime(target_time_str, '%H:%M').time()
    actual = datetime.strptime(actual_time_str, '%H:%M').time()
    
    target_mins = target.hour * 60 + target.minute
    actual_mins = actual.hour * 60 + actual.minute
    
    return abs(target_mins - actual_mins)

def calculate_daily_score():
    """Calculate daily score based on adherence to biological schedule"""
    score = 0
    max_score = 100
    breakdown = {}
    
    today_logs = st.session_state.data.get('today_logs', {})
    profile = st.session_state.data['profile']
    
    # Wake time score (25 points)
    wake_score = 0
    if today_logs.get('wake_time'):
        diff_mins = time_difference_minutes(profile['target_wake_time'], today_logs['wake_time'])
        if diff_mins <= 15:
            wake_score = 25
        elif diff_mins <= 30:
            wake_score = 20
        elif diff_mins <= 60:
            wake_score = 15
        else:
            wake_score = 10
    breakdown['wake_time'] = wake_score
    score += wake_score
    
    # Sleep time score (25 points)
    sleep_score = 0
    if today_logs.get('sleep_time'):
        diff_mins = time_difference_minutes(profile['target_sleep_time'], today_logs['sleep_time'])
        if diff_mins <= 15:
            sleep_score = 25
        elif diff_mins <= 30:
            sleep_score = 20
        elif diff_mins <= 60:
            sleep_score = 15
        else:
            sleep_score = 10
    breakdown['sleep_time'] = sleep_score
    score += sleep_score
    
    # Meal consistency score (30 points - 10 per meal)
    meal_score = 0
    meals = today_logs.get('meals', [])
    if len(meals) >= 3:
        meal_score = 30
    elif len(meals) == 2:
        meal_score = 20
    elif len(meals) == 1:
        meal_score = 10
    breakdown['meals'] = meal_score
    score += meal_score
    
    # Meal quantity appropriateness (10 points)
    quantity_score = 0
    if meals:
        total_quantity = sum(m.get('quantity', 0) for m in meals)
        if 300 <= total_quantity <= 500:
            quantity_score = 10
        elif 200 <= total_quantity <= 600:
            quantity_score = 7
        else:
            quantity_score = 3
    breakdown['meal_quantity'] = quantity_score
    score += quantity_score
    
    # Movement tracking (10 points)
    movement_score = 0
    if st.session_state.last_movement:
        time_since_movement = get_time_since(st.session_state.last_movement)
        if time_since_movement and time_since_movement < timedelta(hours=1):
            movement_score = 10
        elif time_since_movement and time_since_movement < timedelta(hours=2):
            movement_score = 7
        else:
            movement_score = 3
    breakdown['movement'] = movement_score
    score += movement_score
    
    return score, max_score, breakdown

def get_score_grade(score, max_score):
    """Get letter grade based on score percentage"""
    percentage = (score / max_score) * 100
    if percentage >= 90:
        return "A+", "🏆"
    elif percentage >= 80:
        return "A", "⭐"
    elif percentage >= 70:
        return "B", "👍"
    elif percentage >= 60:
        return "C", "📈"
    else:
        return "D", "💪"

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

if 'last_meal_time' not in st.session_state:
    st.session_state.last_meal_time = None

if 'work_session_start' not in st.session_state:
    st.session_state.work_session_start = None

if 'last_movement' not in st.session_state:
    st.session_state.last_movement = None

def get_time_since(past_time):
    """Calculate time difference from now"""
    if past_time is None:
        return None
    now = datetime.now()
    if isinstance(past_time, str):
        past_time = datetime.fromisoformat(past_time)
    diff = now - past_time
    return diff

def format_timedelta(td):
    """Format timedelta for display"""
    if td is None:
        return "Never"
    hours = td.total_seconds() / 3600
    if hours < 1:
        mins = int(td.total_seconds() / 60)
        return f"{mins} minutes"
    return f"{hours:.1f} hours"

def check_alerts():
    """Check for biological condition alerts"""
    alerts = []
    now = datetime.now()
    
    # Alert 1: Meal timing (blood glucose management)
    if st.session_state.last_meal_time:
        time_since_meal = get_time_since(st.session_state.last_meal_time)
        if time_since_meal and time_since_meal > timedelta(hours=4):
            alerts.append({
                'type': 'danger',
                'title': '🚨 GLUCOSE CRASH RISK',
                'message': f"You haven't eaten in {format_timedelta(time_since_meal)}. Your blood glucose is likely dropping, which impairs executive function and decision-making. Eat protein + carbs NOW.",
                'action': 'Log a meal immediately'
            })
        elif time_since_meal and time_since_meal > timedelta(hours=3):
            alerts.append({
                'type': 'warning',
                'title': '⚠️ Time to Eat Soon',
                'message': f"Last meal was {format_timedelta(time_since_meal)} ago. Eat within 30 minutes to prevent glucose crash and maintain cognitive function.",
                'action': 'Prepare a protein-rich snack or meal'
            })
    
    # Alert 2: Work session duration (cognitive exhaustion)
    if st.session_state.work_session_start:
        work_duration = get_time_since(st.session_state.work_session_start)
        if work_duration and work_duration > timedelta(minutes=90):
            alerts.append({
                'type': 'danger',
                'title': '🧠 COGNITIVE EXHAUSTION WARNING',
                'message': f"You've been working for {format_timedelta(work_duration)} without a break. Your prefrontal cortex is depleting glucose and neurotransmitters (dopamine, acetylcholine). Take a 15-20 minute break NOW.",
                'action': 'Log break + light movement'
            })
        elif work_duration and work_duration > timedelta(minutes=75):
            alerts.append({
                'type': 'warning',
                'title': '⏰ Break Time Approaching',
                'message': f"Work session: {format_timedelta(work_duration)}. Plan to take a break in 15 minutes to prevent cognitive depletion.",
                'action': 'Prepare to pause work'
            })
    
    # Alert 3: Movement (adenosine clearing)
    if st.session_state.last_movement:
        time_since_movement = get_time_since(st.session_state.last_movement)
        if time_since_movement and time_since_movement > timedelta(minutes=60):
            alerts.append({
                'type': 'danger',
                'title': '🚶 MOVEMENT REQUIRED',
                'message': f"No movement in {format_timedelta(time_since_movement)}. Adenosine is accumulating, dopamine production is dropping. Stand up and walk for 5 minutes.",
                'action': 'Take a movement break'
            })
        elif time_since_movement and time_since_movement > timedelta(minutes=45):
            alerts.append({
                'type': 'warning',
                'title': '💪 Move Soon',
                'message': f"Last movement: {format_timedelta(time_since_movement)} ago. Get up and move within 15 minutes to prevent fatigue buildup.",
                'action': 'Schedule a stretch break'
            })
    
    # Alert 4: Sleep schedule consistency
    profile = st.session_state.data['profile']
    target_sleep = datetime.strptime(profile['target_sleep_time'], '%H:%M').time()
    current_time = now.time()
    
    # Check if it's past bedtime
    if current_time > target_sleep:
        time_past_bedtime = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), target_sleep)
        if time_past_bedtime > timedelta(minutes=30):
            alerts.append({
                'type': 'warning',
                'title': '😴 Past Your Bedtime',
                'message': f"You're {format_timedelta(time_past_bedtime)} past your target sleep time. Irregular sleep disrupts circadian rhythm and morning cortisol levels.",
                'action': 'Start bedtime routine now'
            })
    
    return alerts

# Sidebar - Profile Setup
with st.sidebar:
    st.markdown("### ⚙️ Your Biological Schedule")
    
    with st.expander("🕐 Sleep & Wake Times", expanded=False):
        wake_time = st.time_input(
            "Target Wake Time",
            value=datetime.strptime(st.session_state.data['profile']['target_wake_time'], '%H:%M').time()
        )
        sleep_time = st.time_input(
            "Target Sleep Time",
            value=datetime.strptime(st.session_state.data['profile']['target_sleep_time'], '%H:%M').time()
        )
        
        if st.button("💾 Save Sleep Schedule"):
            st.session_state.data['profile']['target_wake_time'] = wake_time.strftime('%H:%M')
            st.session_state.data['profile']['target_sleep_time'] = sleep_time.strftime('%H:%M')
            save_data(st.session_state.data)
            st.success("✅ Sleep schedule updated!")
    
    with st.expander("🍽️ Meal Times", expanded=False):
        st.markdown("**Target meal times (prevents glucose crashes)**")
        meal1 = st.time_input("Breakfast", value=datetime.strptime(st.session_state.data['profile']['meal_times'][0], '%H:%M').time())
        meal2 = st.time_input("Lunch", value=datetime.strptime(st.session_state.data['profile']['meal_times'][1], '%H:%M').time())
        meal3 = st.time_input("Dinner", value=datetime.strptime(st.session_state.data['profile']['meal_times'][2], '%H:%M').time())
        
        if st.button("💾 Save Meal Schedule"):
            st.session_state.data['profile']['meal_times'] = [
                meal1.strftime('%H:%M'),
                meal2.strftime('%H:%M'),
                meal3.strftime('%H:%M')
            ]
            save_data(st.session_state.data)
            st.success("✅ Meal schedule updated!")
    
    with st.expander("💼 Work Hours", expanded=False):
        work_start = st.time_input(
            "Work Start",
            value=datetime.strptime(st.session_state.data['profile']['work_start'], '%H:%M').time()
        )
        work_end = st.time_input(
            "Work End",
            value=datetime.strptime(st.session_state.data['profile']['work_end'], '%H:%M').time()
        )
        
        if st.button("💾 Save Work Hours"):
            st.session_state.data['profile']['work_start'] = work_start.strftime('%H:%M')
            st.session_state.data['profile']['work_end'] = work_end.strftime('%H:%M')
            save_data(st.session_state.data)
            st.success("✅ Work hours updated!")

# Main Dashboard
st.markdown('<p class="main-header">🧬 BioRoots Dashboard</p>', unsafe_allow_html=True)
st.markdown("**Evidence-based daily life optimizer addressing biological root causes**")

# Display current time in GMT+3
current_time_gmt3 = get_current_time_gmt3()
st.markdown(f"**Current Time (GMT+3):** {current_time_gmt3.strftime('%H:%M:%S')} | {current_time_gmt3.strftime('%A, %B %d, %Y')}")

st.markdown("---")

# Daily Score Display
st.markdown("### 🎯 Your Daily Score")
score, max_score, breakdown = calculate_daily_score()
grade, emoji = get_score_grade(score, max_score)
percentage = (score / max_score) * 100

col_score1, col_score2, col_score3 = st.columns([2, 2, 3])

with col_score1:
    st.markdown(f"""
    <div class="score-card">
        <div style="font-size: 1.2rem;">Daily Score</div>
        <div class="score-value">{score}/{max_score}</div>
        <div style="font-size: 1.5rem; margin-top: 0.5rem;">{emoji} Grade: {grade}</div>
        <div style="margin-top: 0.5rem; font-size: 0.9rem;">({percentage:.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col_score2:
    st.markdown("#### 📊 Score Breakdown")
    st.metric("⏰ Wake Time", f"{breakdown['wake_time']}/25")
    st.metric("😴 Sleep Time", f"{breakdown['sleep_time']}/25")
    st.metric("🍽️ Meals", f"{breakdown['meals']}/30")

with col_score3:
    st.markdown("#### 💡 How to Improve")
    if breakdown['wake_time'] < 25:
        st.markdown("- ⏰ Wake up closer to your target time")
    if breakdown['sleep_time'] < 25:
        st.markdown("- 😴 Go to sleep closer to your target bedtime")
    if breakdown['meals'] < 30:
        st.markdown("- 🍽️ Log all 3 meals today")
    if breakdown['meal_quantity'] < 10:
        st.markdown("- 📏 Adjust meal quantities (aim for 300-500g total)")
    if breakdown['movement'] < 10:
        st.markdown("- 🚶 Move more frequently (every 45-60 min)")
    if score >= 90:
        st.markdown("- 🏆 **Excellent! Keep it up!**")

st.markdown("---")

# Manual Time Logging Section
st.markdown("### 📝 Manual Time Logging")

col_log1, col_log2, col_log3 = st.columns(3)

with col_log1:
    st.markdown("#### ⏰ Log Wake-Up Time")
    today_logs = st.session_state.data.get('today_logs', {})
    
    current_wake = today_logs.get('wake_time')
    if current_wake:
        st.success(f"✅ Logged: {current_wake}")
    
    wake_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=7, key="wake_hour")
    wake_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0, key="wake_min")
    
    if st.button("💾 Log Wake-Up Time", key="btn_wake"):
        wake_time_str = f"{wake_hour:02d}:{wake_minute:02d}"
        st.session_state.data['today_logs']['wake_time'] = wake_time_str
        st.session_state.data['today_logs']['date'] = current_time_gmt3.date().isoformat()
        save_data(st.session_state.data)
        st.success(f"✅ Wake-up time logged: {wake_time_str}")
        st.rerun()

with col_log2:
    st.markdown("#### 😴 Log Sleep Time")
    
    current_sleep = today_logs.get('sleep_time')
    if current_sleep:
        st.success(f"✅ Logged: {current_sleep}")
    
    sleep_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=23, key="sleep_hour")
    sleep_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0, key="sleep_min")
    
    if st.button("💾 Log Sleep Time", key="btn_sleep"):
        sleep_time_str = f"{sleep_hour:02d}:{sleep_minute:02d}"
        st.session_state.data['today_logs']['sleep_time'] = sleep_time_str
        st.session_state.data['today_logs']['date'] = current_time_gmt3.date().isoformat()
        save_data(st.session_state.data)
        st.success(f"✅ Sleep time logged: {sleep_time_str}")
        st.rerun()

with col_log3:
    st.markdown("#### 🍽️ Log Meal with Quantity")
    
    meal_name = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"], key="meal_type")
    meal_quantity = st.number_input("Quantity (grams)", min_value=10, max_value=1000, value=150, step=10, key="meal_qty")
    meal_composition = st.selectbox(
        "Composition",
        ["Protein-heavy", "Balanced", "Carb-heavy"],
        key="meal_comp"
    )
    
    if st.button("💾 Log Meal", key="btn_meal"):
        if 'meals' not in st.session_state.data['today_logs']:
            st.session_state.data['today_logs']['meals'] = []
        
        meal_entry = {
            'type': meal_name,
            'quantity': meal_quantity,
            'composition': meal_composition,
            'time': current_time_gmt3.strftime('%H:%M')
        }
        st.session_state.data['today_logs']['meals'].append(meal_entry)
        st.session_state.last_meal_time = current_time_gmt3
        save_data(st.session_state.data)
        st.success(f"✅ {meal_name} logged: {meal_quantity}g ({meal_composition})")
        st.rerun()

# Show today's logged meals
if today_logs.get('meals'):
    st.markdown("**Today's Meals:**")
    for idx, meal in enumerate(today_logs['meals']):
        st.markdown(f"- {meal['time']} | {meal['type']}: {meal['quantity']}g ({meal['composition']})")

st.markdown("---")

# Check and display alerts
alerts = check_alerts()
if alerts:
    st.markdown("---")
    for alert in alerts:
        alert_class = f"status-{alert['type']}"
        st.markdown(f"""
        <div class="{alert_class}">
            <h3>{alert['title']}</h3>
            <p><strong>{alert['message']}</strong></p>
            <p style="margin-top: 0.5rem; font-style: italic;">→ {alert['action']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Quick Action Buttons
st.markdown("### ⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🍽️ Log Meal", use_container_width=True):
        st.session_state.last_meal_time = datetime.now()
        st.session_state.data['current_session']['last_meal'] = datetime.now().isoformat()
        save_data(st.session_state.data)
        st.success("✅ Meal logged!")
        st.rerun()

with col2:
    if st.session_state.work_session_start is None:
        if st.button("▶️ Start Work Session", use_container_width=True):
            st.session_state.work_session_start = datetime.now()
            st.session_state.data['current_session']['work_start'] = datetime.now().isoformat()
            save_data(st.session_state.data)
            st.success("✅ Work session started!")
            st.rerun()
    else:
        if st.button("⏸️ Take Break", use_container_width=True):
            st.session_state.work_session_start = None
            st.session_state.data['current_session']['work_start'] = None
            save_data(st.session_state.data)
            st.success("✅ Break time! Rest for 15-20 minutes.")
            st.rerun()

with col3:
    if st.button("🚶 Log Movement", use_container_width=True):
        st.session_state.last_movement = datetime.now()
        st.session_state.data['current_session']['last_movement'] = datetime.now().isoformat()
        save_data(st.session_state.data)
        st.success("✅ Movement logged!")
        st.rerun()

with col4:
    if st.button("☀️ Log Sunlight", use_container_width=True):
        if 'sunlight_exposure' not in st.session_state.data['current_session']:
            st.session_state.data['current_session']['sunlight_exposure'] = []
        st.session_state.data['current_session']['sunlight_exposure'].append(datetime.now().isoformat())
        save_data(st.session_state.data)
        st.success("✅ Sunlight exposure logged!")
        st.rerun()

st.markdown("---")

# Dashboard Metrics
st.markdown("### 📊 Current Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### 🍽️ Blood Glucose Management")
    
    if st.session_state.last_meal_time:
        time_since_meal = get_time_since(st.session_state.last_meal_time)
        hours_since = time_since_meal.total_seconds() / 3600 if time_since_meal else 0
        
        if hours_since < 3:
            status_color = "🟢"
            status_text = "Good"
        elif hours_since < 4:
            status_color = "🟡"
            status_text = "Caution"
        else:
            status_color = "🔴"
            status_text = "Critical"
        
        st.markdown(f"**Status:** {status_color} {status_text}")
        st.markdown(f"**Last meal:** {format_timedelta(time_since_meal)} ago")
    else:
        st.markdown("**Status:** 🔴 No meal logged today")
        st.markdown("**Action:** Log your last meal or eat now")
    
    st.markdown("**Why it matters:** Glucose fuels your prefrontal cortex. Drops cause procrastination, poor decisions, and cognitive fatigue.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### 🧠 Cognitive Load Management")
    
    if st.session_state.work_session_start:
        work_duration = get_time_since(st.session_state.work_session_start)
        minutes_working = work_duration.total_seconds() / 60 if work_duration else 0
        
        if minutes_working < 75:
            status_color = "🟢"
            status_text = "Optimal"
            remaining = 90 - minutes_working
            st.markdown(f"**Status:** {status_color} {status_text}")
            st.markdown(f"**Working for:** {format_timedelta(work_duration)}")
            st.markdown(f"**Break in:** {int(remaining)} minutes")
        elif minutes_working < 90:
            status_color = "🟡"
            status_text = "Break Soon"
            st.markdown(f"**Status:** {status_color} {status_text}")
            st.markdown(f"**Working for:** {format_timedelta(work_duration)}")
            st.markdown("**Action:** Prepare to take a break")
        else:
            status_color = "🔴"
            status_text = "Overworked"
            st.markdown(f"**Status:** {status_color} {status_text}")
            st.markdown(f"**Working for:** {format_timedelta(work_duration)}")
            st.markdown("**Action:** TAKE BREAK NOW")
    else:
        st.markdown("**Status:** 🔵 Not in work session")
        st.markdown("**Action:** Start work session when you begin focused work")
    
    st.markdown("**Why it matters:** 90-min cycles prevent neurotransmitter depletion (dopamine, acetylcholine). Prevents decision fatigue.")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### 💪 Movement & Adenosine Clearing")
    
    if st.session_state.last_movement:
        time_since_movement = get_time_since(st.session_state.last_movement)
        minutes_since = time_since_movement.total_seconds() / 60 if time_since_movement else 0
        
        if minutes_since < 45:
            status_color = "🟢"
            status_text = "Active"
        elif minutes_since < 60:
            status_color = "🟡"
            status_text = "Move Soon"
        else:
            status_color = "🔴"
            status_text = "Too Sedentary"
        
        st.markdown(f"**Status:** {status_color} {status_text}")
        st.markdown(f"**Last movement:** {format_timedelta(time_since_movement)} ago")
    else:
        st.markdown("**Status:** 🔴 No movement logged")
        st.markdown("**Action:** Log movement or take a walk")
    
    st.markdown("**Why it matters:** Movement clears adenosine (reduces fatigue), boosts dopamine (motivation), improves glucose utilization.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Additional tracking areas
st.markdown("### 🎯 Additional Biological Areas")

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("😴 Sleep Quality & Consistency"):
        st.markdown("#### Track Sleep")
        
        profile = st.session_state.data['profile']
        target_wake = datetime.strptime(profile['target_wake_time'], '%H:%M').time()
        target_sleep = datetime.strptime(profile['target_sleep_time'], '%H:%M').time()
        
        st.markdown(f"**Target sleep:** {target_sleep.strftime('%I:%M %p')}")
        st.markdown(f"**Target wake:** {target_wake.strftime('%I:%M %p')}")
        
        actual_sleep = st.time_input("Actual bedtime last night", value=target_sleep)
        actual_wake = st.time_input("Actual wake time today", value=target_wake)
        sleep_quality = st.slider("Sleep quality (1-10)", 1, 10, 7)
        
        if st.button("Log Sleep Data"):
            today = datetime.now().date().isoformat()
            sleep_log = {
                'date': today,
                'actual_sleep': actual_sleep.strftime('%H:%M'),
                'actual_wake': actual_wake.strftime('%H:%M'),
                'quality': sleep_quality
            }
            st.session_state.data['daily_logs'].append({
                'type': 'sleep',
                'data': sleep_log
            })
            save_data(st.session_state.data)
            st.success("✅ Sleep data logged!")
        
        st.markdown("---")
        st.markdown("**Biological impact:**")
        st.markdown("- Inconsistent sleep → circadian disruption → unpredictable cortisol")
        st.markdown("- Poor sleep → low morning cortisol → difficulty waking")
        st.markdown("- Sleep debt → adenosine accumulation → constant fatigue")

with col2:
    with st.expander("☀️ Light Exposure & Circadian Health"):
        st.markdown("#### Track Sunlight")
        
        sunlight_count = len(st.session_state.data['current_session'].get('sunlight_exposure', []))
        
        if sunlight_count == 0:
            st.markdown("**Status:** 🔴 No sunlight today")
        elif sunlight_count < 2:
            st.markdown(f"**Status:** 🟡 {sunlight_count} exposure(s)")
        else:
            st.markdown(f"**Status:** 🟢 {sunlight_count} exposure(s)")
        
        st.markdown("**Target:** 2-3 outdoor exposures per day")
        st.markdown("- Morning (within 1hr of waking): Critical for cortisol rhythm")
        st.markdown("- Midday: Boost alertness")
        st.markdown("- Afternoon: Support evening melatonin timing")
        
        outdoor_duration = st.number_input("Minutes spent outdoors today", min_value=0, max_value=480, value=0, step=5)
        
        if st.button("Log Outdoor Time"):
            st.session_state.data['daily_logs'].append({
                'type': 'outdoor',
                'data': {
                    'date': datetime.now().date().isoformat(),
                    'duration': outdoor_duration
                }
            })
            save_data(st.session_state.data)
            st.success("✅ Outdoor time logged!")
        
        st.markdown("---")
        st.markdown("**Biological impact:**")
        st.markdown("- No morning light → circadian desynchronization")
        st.markdown("- Indoor work → melatonin dysregulation → poor sleep")
        st.markdown("- Low light → serotonin drops → mood/motivation decline")

with col3:
    with st.expander("🍴 Meal Type & Timing Strategy"):
        st.markdown("#### Log Detailed Meal")
        
        meal_type = st.selectbox("Meal type", ["Breakfast", "Lunch", "Dinner", "Snack"])
        meal_composition = st.selectbox(
            "Primary composition",
            ["Protein-heavy (best for focus)", "Balanced (protein + carbs)", "Carb-heavy (causes sleepiness)"]
        )
        
        if st.button("Log Meal Details"):
            st.session_state.last_meal_time = datetime.now()
            st.session_state.data['daily_logs'].append({
                'type': 'meal',
                'data': {
                    'time': datetime.now().isoformat(),
                    'meal_type': meal_type,
                    'composition': meal_composition
                }
            })
            save_data(st.session_state.data)
            st.success("✅ Meal details logged!")
        
        st.markdown("---")
        st.markdown("**Timing strategy:**")
        st.markdown("- **Before focused work:** Protein-heavy (stable glucose)")
        st.markdown("- **During work:** Small protein snacks (maintain neurotransmitters)")
        st.markdown("- **After work:** Carbs OK (serotonin/melatonin won't hurt evening)")
        
        st.markdown("**Why composition matters:**")
        st.markdown("- Carbs → insulin surge → tryptophan → melatonin → sleepiness")
        st.markdown("- Protein → stable glucose → sustained executive function")

st.markdown("---")

# Daily summary and patterns
st.markdown("### 📈 Today's Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    meal_logs = [log for log in st.session_state.data['daily_logs'] if log['type'] == 'meal']
    today_meals = [log for log in meal_logs if log['data']['time'].startswith(datetime.now().date().isoformat())]
    st.metric("🍽️ Meals Logged", len(today_meals), help="Target: 3 main meals")

with col2:
    sunlight_exposures = len(st.session_state.data['current_session'].get('sunlight_exposure', []))
    st.metric("☀️ Sunlight Exposures", sunlight_exposures, help="Target: 2-3 times/day")

with col3:
    if st.session_state.work_session_start:
        work_time = get_time_since(st.session_state.work_session_start)
        work_mins = int(work_time.total_seconds() / 60) if work_time else 0
    else:
        work_mins = 0
    st.metric("⏱️ Current Work Session", f"{work_mins} min", help="Target: 90-min cycles")

with col4:
    if st.session_state.last_movement:
        time_since = get_time_since(st.session_state.last_movement)
        mins_since = int(time_since.total_seconds() / 60) if time_since else 999
        delta_color = "inverse" if mins_since > 45 else "normal"
    else:
        mins_since = 999
        delta_color = "inverse"
    st.metric("🚶 Minutes Since Movement", mins_since, delta=f"Target: <45", delta_color=delta_color)

st.markdown("---")

# Educational section
with st.expander("📚 Understanding the 9 Biological Root Causes"):
    st.markdown("""
    ### The Science Behind BioRoots
    
    This app addresses **9 biological root causes** that affect daily performance:
    
    #### Currently Tracked (MVP):
    
    1. **Sleep Quality & Consistency** 
       - *Biology:* Inconsistent sleep → circadian disruption → cortisol dysregulation → energy crashes
       - *Solution:* Track consistency, enforce bedtime, monitor quality
    
    2. **Blood Glucose Management (Meal Timing)**
       - *Biology:* Skipped meals → glucose drops → prefrontal cortex impairment → procrastination
       - *Solution:* Meal reminders BEFORE hunger, track timing, prevent 4hr+ gaps
    
    3. **Cognitive Load Cycles**
       - *Biology:* 90+ min work → glucose depletion → neurotransmitter drop → decision fatigue
       - *Solution:* Enforce 90-min work cycles, mandatory breaks, snack reminders
    
    4. **Movement & Adenosine Clearing**
       - *Biology:* Sedentary → adenosine accumulates → fatigue builds → dopamine drops
       - *Solution:* Movement every 45-60min, track activity, clear adenosine
    
    5. **Light Exposure & Circadian Health**
       - *Biology:* No sunlight → circadian desynchronization → melatonin dysregulation → poor sleep
       - *Solution:* Morning sunlight tracking, outdoor time goals
    
    #### Coming Soon (Expansion):
    
    6. **Difficulty Waking Up**
       - Morning cortisol optimization, wake time consistency enforcement
    
    7. **Focus-Breakthrough Sleep Impulse**
       - Intense focus detection, movement triggers during deep work
    
    8. **Decision Fatigue Tracking**
       - Decision limit counter, decision-heavy vs decision-light time blocks
    
    9. **Irregular Work Schedule**
       - Work time consistency tracking, schedule deviation logging
    
    ---
    
    ### Key Principle: Biology, Not Willpower
    
    Most productivity advice relies on willpower and discipline. **This fails** because:
    
    - Low glucose → impaired prefrontal cortex → no willpower available
    - Sleep deprivation → adenosine accumulation → constant fatigue
    - Neurotransmitter depletion → motivation collapse
    
    **BioRoots instead** uses preventive alerts based on biological timers:
    - Alert you BEFORE glucose crashes (not after you're already tired)
    - Enforce breaks BEFORE neurotransmitter depletion
    - Track patterns to fix circadian rhythm issues
    
    This works with your biology, not against it.
    """)

# Footer
st.markdown("---")
st.markdown("**🧬 BioRoots** - Evidence-based daily optimization | Built on biological science, not willpower")
