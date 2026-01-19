import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Clock, Moon, Sun, Coffee, Utensils, Activity, AlertCircle, CheckCircle, Plus, X, Edit2 } from 'lucide-react';

interface SleepData {
  bedTime: Date | null;
  wakeTime: Date | null;
  quality: number | null;
  isAsleep: boolean;
}

interface Meal {
  id: number;
  name: string;
  ingredients: string;
  calories: number;
  quantity: number;
  type: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  composition: 'protein-heavy' | 'balanced' | 'carb-heavy';
  time: Date;
  analysis?: MealAnalysis;
}

interface MealAnalysis {
  biologyLevel: string;
  impactScore: number;
  problems: string[];
  benefits: string[];
  recommendations: string[];
}

interface WorkSession {
  id: number;
  startTime: Date;
  endTime: Date | null;
}

interface Movement {
  id: number;
  time: Date;
}

interface SunlightExposure {
  id: number;
  time: Date;
  duration: number;
}

interface BioAlert {
  id: string;
  type: 'warning' | 'critical';
  title: string;
  message: string;
  biology: string;
}

const BioRootsTracker: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [sleepData, setSleepData] = useState<SleepData>({
    bedTime: null,
    wakeTime: null,
    quality: null,
    isAsleep: false
  });
  const [meals, setMeals] = useState<Meal[]>([]);
  const [workSessions, setWorkSessions] = useState<WorkSession[]>([]);
  const [movements, setMovements] = useState<Movement[]>([]);
  const [sunlightExposure, setSunlightExposure] = useState<SunlightExposure[]>([]);
  const [alerts, setAlerts] = useState<BioAlert[]>([]);
  const [showMealForm, setShowMealForm] = useState(false);
  const [showTimeInput, setShowTimeInput] = useState<{ type: string | null; action: string | null }>({ 
    type: null, 
    action: null 
  });
  const [manualTime, setManualTime] = useState('');
  const [dailyScore, setDailyScore] = useState(0);
  
  // Meal form state
  const [mealForm, setMealForm] = useState({
    name: '',
    ingredients: '',
    calories: 400,
    quantity: 200,
    type: 'breakfast' as 'breakfast' | 'lunch' | 'dinner' | 'snack',
    composition: 'balanced' as 'protein-heavy' | 'balanced' | 'carb-heavy'
  });

  // Update current time every minute
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  // Check for biological alerts
  useEffect(() => {
    checkBiologicalAlerts();
  }, [currentTime, meals, workSessions, movements, sleepData]);

  // Calculate daily score
  useEffect(() => {
    calculateDailyScore();
  }, [sleepData, meals, movements]);

  const analyzeMealBiology = (meal: Omit<Meal, 'id' | 'time' | 'analysis'>): MealAnalysis => {
    let impactScore = 100;
    const problems: string[] = [];
    const benefits: string[] = [];
    const recommendations: string[] = [];

    const ingredients = meal.ingredients.toLowerCase();
    
    // Check for high-GI carbs
    const highGICarbs = ['white bread', 'rice', 'pasta', 'sugar', 'candy', 'soda'];
    const hasHighGI = highGICarbs.some(carb => ingredients.includes(carb));
    
    // Check for protein
    const proteinSources = ['chicken', 'beef', 'fish', 'egg', 'protein', 'tofu'];
    const hasProtein = proteinSources.some(protein => ingredients.includes(protein));

    // Calorie analysis
    if (meal.type === 'snack') {
      if (meal.calories > 300) {
        problems.push(`⚠️ High calories for snack (${meal.calories} kcal) - May cause insulin spike`);
        impactScore -= 15;
      } else if (meal.calories < 100) {
        benefits.push(`✅ Light snack (${meal.calories} kcal) - Won't disrupt glucose balance`);
      }
    } else {
      if (meal.calories < 300) {
        problems.push(`⚠️ Low calories (${meal.calories} kcal) - May cause hunger in 2-3 hours`);
        impactScore -= 10;
      } else if (meal.calories > 800) {
        problems.push(`⚠️ High calories (${meal.calories} kcal) - Large insulin response`);
        impactScore -= 15;
      } else if (meal.calories >= 400 && meal.calories <= 600) {
        benefits.push(`✅ Optimal calories (${meal.calories} kcal) - Sustained energy`);
        impactScore += 10;
      }
    }

    // Composition analysis
    if (hasHighGI && meal.composition !== 'protein-heavy') {
      problems.push('🔴 GLUCOSE SPIKE RISK - Refined carbs without protein buffer');
      problems.push('   → Insulin surge → Tryptophan → Serotonin/Melatonin → SLEEPINESS');
      impactScore -= 20;
    }

    if (!hasProtein) {
      problems.push('⚠️ Low protein - May not sustain cognitive function');
      impactScore -= 15;
    } else {
      benefits.push('✅ Contains protein - Supports neurotransmitter production');
      impactScore += 10;
    }

    // Timing analysis
    const currentHour = new Date().getHours();
    if (meal.type === 'lunch' && currentHour >= 12 && currentHour <= 14) {
      if (meal.composition === 'carb-heavy') {
        problems.push('🔴 AFTERNOON SLUMP RISK - Carb-heavy lunch during work hours');
        impactScore -= 25;
      } else if (meal.composition === 'protein-heavy') {
        benefits.push('✅ Protein-rich lunch - Maintains alertness through afternoon dip');
        impactScore += 15;
      }
    }

    // Quantity analysis
    if (meal.quantity > 500) {
      problems.push(`⚠️ Large portion (${meal.quantity}g) - May divert blood from brain`);
      impactScore -= 10;
    }

    // Recommendations
    if (meal.composition === 'carb-heavy' && currentHour >= 9 && currentHour <= 17) {
      recommendations.push('💡 Save carb-heavy meals for evening to avoid daytime drowsiness');
    }
    if (!hasProtein && (meal.type === 'breakfast' || meal.type === 'lunch')) {
      recommendations.push('💡 Add protein source (eggs, chicken, fish) to sustain energy');
    }
    if (hasHighGI) {
      recommendations.push('💡 Pair carbs with protein/fat to slow absorption');
    }

    // Determine biology level
    impactScore = Math.max(0, Math.min(100, impactScore));
    let biologyLevel = '';
    if (impactScore >= 85) biologyLevel = '🏆 OPTIMAL - Excellent biological support';
    else if (impactScore >= 70) biologyLevel = '✅ GOOD - Positive biological impact';
    else if (impactScore >= 50) biologyLevel = '⚠️ MODERATE - Some biological concerns';
    else biologyLevel = '🔴 POOR - Significant biological issues';

    return { biologyLevel, impactScore, problems, benefits, recommendations };
  };

  const calculateDailyScore = () => {
    let score = 0;
    
    // Wake time consistency (25 points)
    if (sleepData.wakeTime) score += 20;
    
    // Sleep time consistency (25 points)
    if (sleepData.bedTime) score += 20;
    
    // Meals (30 points)
    if (meals.length >= 3) score += 30;
    else if (meals.length === 2) score += 20;
    else if (meals.length === 1) score += 10;
    
    // Movement (10 points)
    if (movements.length > 0) {
      const lastMovement = movements[movements.length - 1];
      const hoursSince = (new Date().getTime() - lastMovement.time.getTime()) / (1000 * 60 * 60);
      if (hoursSince < 1) score += 10;
      else if (hoursSince < 2) score += 7;
      else score += 3;
    }
    
    // Meal quality (15 points)
    const avgMealScore = meals.reduce((acc, meal) => 
      acc + (meal.analysis?.impactScore || 50), 0) / (meals.length || 1);
    score += Math.round((avgMealScore / 100) * 15);
    
    setDailyScore(score);
  };

  const checkBiologicalAlerts = () => {
    const newAlerts: BioAlert[] = [];
    const now = new Date();

    // Meal timing check
    if (meals.length > 0) {
      const lastMeal = meals[meals.length - 1];
      const hoursSinceLastMeal = (now.getTime() - lastMeal.time.getTime()) / (1000 * 60 * 60);
      
      if (hoursSinceLastMeal >= 3.5 && hoursSinceLastMeal < 4) {
        newAlerts.push({
          id: 'pre-glucose-drop',
          type: 'warning',
          title: 'Preventive Meal Alert',
          message: "It's been 3.5 hours since your last meal. Eat NOW before glucose drops.",
          biology: 'Glucose drop → prefrontal cortex impairment → procrastination & poor decisions'
        });
      } else if (hoursSinceLastMeal >= 4) {
        newAlerts.push({
          id: 'glucose-critical',
          type: 'critical',
          title: 'CRITICAL: Glucose Management',
          message: '4+ hours without food! Your decision-making is already impaired.',
          biology: 'Blood glucose too low → cognitive function compromised'
        });
      }
    }

    // Work session check
    const activeSession = workSessions.find(s => !s.endTime);
    if (activeSession) {
      const sessionMinutes = (now.getTime() - activeSession.startTime.getTime()) / (1000 * 60);
      
      if (sessionMinutes >= 85 && sessionMinutes < 90) {
        newAlerts.push({
          id: 'work-break-warning',
          type: 'warning',
          title: 'Break Time Approaching',
          message: "You've been working for 85 minutes. Prepare to take a break.",
          biology: 'Approaching neurotransmitter depletion threshold'
        });
      } else if (sessionMinutes >= 90) {
        newAlerts.push({
          id: 'work-break-critical',
          type: 'critical',
          title: 'MANDATORY BREAK',
          message: '90+ minutes of work! Take a break NOW to prevent decision fatigue.',
          biology: 'Glucose depletion → neurotransmitter drop → decision fatigue'
        });
      }
    }

    // Movement check
    if (movements.length > 0) {
      const lastMovement = movements[movements.length - 1];
      const minutesSinceMovement = (now.getTime() - lastMovement.time.getTime()) / (1000 * 60);
      
      if (minutesSinceMovement >= 60) {
        newAlerts.push({
          id: 'movement-required',
          type: 'warning',
          title: 'Movement Required',
          message: '60+ minutes sedentary. Move now to clear adenosine buildup.',
          biology: 'Sedentary → adenosine accumulates → fatigue builds → dopamine drops'
        });
      }
    }

    setAlerts(newAlerts);
  };

  const handleSleepAction = (action: 'sleep' | 'wake') => {
    setShowTimeInput({ type: 'sleep', action });
  };

  const confirmTimeInput = () => {
    const time = manualTime ? 
      new Date(`${new Date().toDateString()} ${manualTime}`) : 
      new Date();
    
    if (showTimeInput.type === 'sleep') {
      if (showTimeInput.action === 'sleep') {
        setSleepData(prev => ({ ...prev, bedTime: time, isAsleep: true }));
      } else if (showTimeInput.action === 'wake') {
        setSleepData(prev => ({ ...prev, wakeTime: time, isAsleep: false }));
      }
    } else if (showTimeInput.type === 'meal') {
      const analysis = analyzeMealBiology(mealForm);
      const newMeal: Meal = {
        ...mealForm,
        time: time,
        id: Date.now(),
        analysis
      };
      setMeals(prev => [...prev, newMeal]);
      setMealForm({ 
        name: '', 
        ingredients: '', 
        calories: 400,
        quantity: 200,
        type: 'breakfast', 
        composition: 'balanced' 
      });
      setShowMealForm(false);
    } else if (showTimeInput.type === 'work') {
      if (showTimeInput.action === 'start') {
        setWorkSessions(prev => [...prev, { startTime: time, endTime: null, id: Date.now() }]);
      } else {
        setWorkSessions(prev => prev.map(session => 
          !session.endTime ? { ...session, endTime: time } : session
        ));
      }
    } else if (showTimeInput.type === 'movement') {
      setMovements(prev => [...prev, { time: time, id: Date.now() }]);
    } else if (showTimeInput.type === 'sunlight') {
      setSunlightExposure(prev => [...prev, { time: time, duration: 15, id: Date.now() }]);
    }
    
    setShowTimeInput({ type: null, action: null });
    setManualTime('');
  };

  const formatTime = (date: Date | null) => {
    if (!date) return '--:--';
    return new Date(date).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  const formatDuration = (start: Date | null, end: Date | null) => {
    if (!start || !end) return '--';
    const minutes = Math.round((end.getTime() - start.getTime()) / (1000 * 60));
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const getScoreGrade = (score: number) => {
    if (score >= 90) return { grade: 'A+', emoji: '🏆', color: 'text-green-400' };
    if (score >= 80) return { grade: 'A', emoji: '⭐', color: 'text-green-300' };
    if (score >= 70) return { grade: 'B', emoji: '👍', color: 'text-yellow-400' };
    if (score >= 60) return { grade: 'C', emoji: '📈', color: 'text-yellow-300' };
    return { grade: 'D', emoji: '💪', color: 'text-red-400' };
  };

  const activeWorkSession = workSessions.find(s => !s.endTime);
  const scoreInfo = getScoreGrade(dailyScore);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-6xl mx-auto space-y-4">
        {/* Header with Score */}
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-white mb-2">🧬 BioRoots Tracker</h1>
          <p className="text-purple-200">Biology-Based Performance Optimization</p>
          <p className="text-purple-300 text-sm mt-1">{currentTime.toLocaleString()}</p>
          
          {/* Daily Score */}
          <div className="mt-4 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg p-4 max-w-md mx-auto">
            <div className="text-white text-sm">Daily Score</div>
            <div className={`text-5xl font-bold ${scoreInfo.color}`}>
              {dailyScore}/100
            </div>
            <div className="text-white text-2xl mt-2">
              {scoreInfo.emoji} Grade: {scoreInfo.grade}
            </div>
          </div>
        </div>

        {/* Alerts Section */}
        {alerts.length > 0 && (
          <div className="space-y-2">
            {alerts.map(alert => (
              <Alert key={alert.id} className={`${
                alert.type === 'critical' 
                  ? 'bg-red-900/50 border-red-500 text-red-100' 
                  : 'bg-yellow-900/50 border-yellow-500 text-yellow-100'
              }`}>
                <AlertCircle className="h-4 w-4" />
                <div>
                  <div className="font-bold">{alert.title}</div>
                  <AlertDescription className="text-sm mt-1">
                    {alert.message}
                    <div className="text-xs mt-1 opacity-80 italic">🧬 {alert.biology}</div>
                  </AlertDescription>
                </div>
              </Alert>
            ))}
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-4">
          {/* Sleep Tracking */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Moon className="h-5 w-5 text-purple-400" />
                Sleep Quality & Consistency
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-purple-200 text-sm mb-3">
                <strong>Biology:</strong> Inconsistent sleep → circadian disruption → cortisol dysregulation
              </div>
              
              <div className="flex gap-2">
                <Button 
                  onClick={() => handleSleepAction('sleep')}
                  disabled={sleepData.isAsleep}
                  className="flex-1 bg-purple-600 hover:bg-purple-700"
                >
                  <Moon className="h-4 w-4 mr-2" />
                  {sleepData.isAsleep ? 'Sleeping...' : 'Go to Sleep'}
                </Button>
                <Button 
                  onClick={() => handleSleepAction('wake')}
                  disabled={!sleepData.isAsleep}
                  className="flex-1 bg-amber-600 hover:bg-amber-700"
                >
                  <Sun className="h-4 w-4 mr-2" />
                  Wake Up
                </Button>
              </div>

              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="bg-slate-700/50 p-2 rounded">
                  <div className="text-purple-300">Bedtime</div>
                  <div className="text-white font-bold">{formatTime(sleepData.bedTime)}</div>
                </div>
                <div className="bg-slate-700/50 p-2 rounded">
                  <div className="text-amber-300">Wake Time</div>
                  <div className="text-white font-bold">{formatTime(sleepData.wakeTime)}</div>
                </div>
              </div>

              {sleepData.bedTime && sleepData.wakeTime && (
                <div className="bg-green-900/30 p-2 rounded text-sm text-green-200">
                  Sleep Duration: {formatDuration(sleepData.bedTime, sleepData.wakeTime)}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Meal Tracking with Analysis */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Utensils className="h-5 w-5 text-green-400" />
                Meal Analysis & Glucose Management
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-green-200 text-sm mb-3">
                <strong>Biology:</strong> Skipped meals → glucose drops → prefrontal cortex impairment
              </div>

              <Button 
                onClick={() => setShowMealForm(true)}
                className="w-full bg-green-600 hover:bg-green-700"
              >
                <Plus className="h-4 w-4 mr-2" />
                Log & Analyze Meal
              </Button>

              {showMealForm && (
                <div className="bg-slate-700/50 p-3 rounded space-y-2">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="text-white font-semibold">Add Meal Details</h4>
                    <Button 
                      size="sm" 
                      variant="ghost" 
                      onClick={() => setShowMealForm(false)}
                      className="text-white"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                  
                  <input
                    type="text"
                    placeholder="Meal name (e.g., Chicken Salad)"
                    value={mealForm.name}
                    onChange={(e) => setMealForm(prev => ({ ...prev, name: e.target.value }))}
                    className="w-full p-2 rounded bg-slate-600 text-white placeholder-slate-400"
                  />
                  
                  <textarea
                    placeholder="Ingredients (e.g., chicken breast, lettuce, tomatoes, olive oil)"
                    value={mealForm.ingredients}
                    onChange={(e) => setMealForm(prev => ({ ...prev, ingredients: e.target.value }))}
                    className="w-full p-2 rounded bg-slate-600 text-white placeholder-slate-400 min-h-20"
                  />
                  
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="number"
                      placeholder="Calories (kcal)"
                      value={mealForm.calories}
                      onChange={(e) => setMealForm(prev => ({ ...prev, calories: parseInt(e.target.value) || 0 }))}
                      className="w-full p-2 rounded bg-slate-600 text-white"
                    />
                    <input
                      type="number"
                      placeholder="Quantity (g)"
                      value={mealForm.quantity}
                      onChange={(e) => setMealForm(prev => ({ ...prev, quantity: parseInt(e.target.value) || 0 }))}
                      className="w-full p-2 rounded bg-slate-600 text-white"
                    />
                  </div>
                  
                  <select
                    value={mealForm.type}
                    onChange={(e) => setMealForm(prev => ({ ...prev, type: e.target.value as any }))}
                    className="w-full p-2 rounded bg-slate-600 text-white"
                  >
                    <option value="breakfast">Breakfast</option>
                    <option value="lunch">Lunch</option>
                    <option value="dinner">Dinner</option>
                    <option value="snack">Snack</option>
                  </select>

                  <select
                    value={mealForm.composition}
                    onChange={(e) => setMealForm(prev => ({ ...prev, composition: e.target.value as any }))}
                    className="w-full p-2 rounded bg-slate-600 text-white"
                  >
                    <option value="protein-heavy">Protein-heavy</option>
                    <option value="balanced">Balanced</option>
                    <option value="carb-heavy">Carb-heavy</option>
                  </select>

                  <Button 
                    onClick={() => setShowTimeInput({ type: 'meal', action: 'add' })}
                    className="w-full bg-green-600 hover:bg-green-700"
                    disabled={!mealForm.name || !mealForm.ingredients}
                  >
                    <Clock className="h-4 w-4 mr-2" />
                    Set Time & Analyze
                  </Button>
                </div>
              )}

              <div className="max-h-48 overflow-y-auto space-y-2">
                {meals.slice(-3).reverse().map(meal => (
                  <div key={meal.id} className="bg-slate-700/50 p-2 rounded text-sm">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="text-white font-semibold">{meal.name}</div>
                        <div className="text-green-300 text-xs">{meal.calories} kcal | {meal.quantity}g</div>
                        {meal.analysis && (
                          <div className="text-xs mt-1">
                            <div className="text-blue-400">{meal.analysis.biologyLevel}</div>
                            <div className="text-yellow-300">Score: {meal.analysis.impactScore}/100</div>
                          </div>
                        )}
                      </div>
                      <div className="text-green-400 text-xs">{formatTime(meal.time)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Work Sessions */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Coffee className="h-5 w-5 text-blue-400" />
                Cognitive Load Cycles
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-blue-200 text-sm mb-3">
                <strong>Biology:</strong> 90+ min work → glucose depletion → decision fatigue
              </div>

              <div className="flex gap-2">
                <Button 
                  onClick={() => setShowTimeInput({ type: 'work', action: 'start' })}
                  disabled={!!activeWorkSession}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  Start Work
                </Button>
                <Button 
                  onClick={() => setShowTimeInput({ type: 'work', action: 'end' })}
                  disabled={!activeWorkSession}
                  className="flex-1 bg-red-600 hover:bg-red-700"
                >
                  End Session
                </Button>
              </div>

              {activeWorkSession && (
                <div className="bg-blue-900/30 p-3 rounded">
                  <div className="text-blue-200 text-sm">Active Session</div>
                  <div className="text-white font-bold">
                    {Math.round((new Date().getTime() - activeWorkSession.startTime.getTime()) / (1000 * 60))} minutes
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Movement & Sunlight */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Activity className="h-5 w-5 text-red-400" />
                Movement & Sunlight
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-red-200 text-sm mb-3">
                <strong>Biology:</strong> Sedentary → adenosine accumulates → fatigue builds
              </div>

              <div className="flex gap-2">
                <Button 
                  onClick={() => setShowTimeInput({ type: 'movement', action: 'log' })}
                  className="flex-1 bg-red-600 hover:bg-red-700"
                >
                  <Activity className="h-4 w-4 mr-2" />
                  Log Movement
                </Button>
                <Button 
                  onClick={() => setShowTimeInput({ type: 'sunlight', action: 'log' })}
                  className="flex-1 bg-yellow-600 hover:bg-yellow-700"
                >
                  <Sun className="h-4 w-4 mr-2" />
                  Log Sunlight
                </Button>
              </div>

              {movements.length > 0 && (
                <div className="bg-red-900/30 p-2 rounded text-sm">
                  <div className="text-red-200">Last movement:</div>
                  <div className="text-white font-bold">
                    {Math.round((new Date().getTime() - movements[movements.length - 1].time.getTime()) / (1000 * 60))} min ago
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Time Input Modal */}
        {showTimeInput.type && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <Card className="bg-slate-800 border-slate-700 max-w-md w-full">
              <CardHeader>
                <CardTitle className="text-white">Set Time</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Button 
                    onClick={confirmTimeInput}
                    className="w-full bg-green-600 hover:bg-green-700"
                  >
                    Use Current Time
                  </Button>
                  <div className="text-center text-slate-400 text-sm">or</div>
                  <input
                    type="time"
                    value={manualTime}
                    onChange={(e) => setManualTime(e.target.value)}
                    className="w-full p-2 rounded bg-slate-700 text-white"
                  />
                  <Button 
                    onClick={confirmTimeInput}
                    disabled={!manualTime}
                    className="w-full bg-blue-600 hover:bg-blue-700"
                  >
                    Use Manual Time
                  </Button>
                </div>
                <Button 
                  onClick={() => {
                    setShowTimeInput({ type: null, action: null });
                    setManualTime('');
                  }}
                  variant="outline"
                  className="w-full"
                >
                  Cancel
                </Button>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Biology Principles Footer */}
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white text-sm">🧬 Key Principle: Biology, Not Willpower</CardTitle>
          </CardHeader>
          <CardContent className="text-slate-300 text-xs space-y-1">
            <p>• Low glucose → impaired prefrontal cortex → no willpower available</p>
            <p>• Sleep deprivation → adenosine accumulation → constant fatigue</p>
            <p>• Neurotransmitter depletion → motivation collapse</p>
            <p className="text-green-400 mt-2">✓ This tracker alerts you BEFORE biological failures occur</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default BioRootsTracker;
