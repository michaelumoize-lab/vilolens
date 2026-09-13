"use client";

import { useState } from "react";

// Feature definitions with realistic bounds based on Wine Quality dataset
interface FeatureConfig {
  key: string;
  label: string;
  unit: string;
  min: number;
  max: number;
  step: number;
  description: string;
}

const FEATURES: FeatureConfig[] = [
  { key: "alcohol", label: "Alcohol", unit: "% vol", min: 8.0, max: 15.0, step: 0.1, description: "Alcohol percentage by volume" },
  { key: "volatile_acidity", label: "Volatile Acidity", unit: "g/dm³", min: 0.1, max: 1.6, step: 0.01, description: "Acetic acid amount (vinegar aroma)" },
  { key: "sulphates", label: "Sulphates", unit: "g/dm³", min: 0.3, max: 2.0, step: 0.01, description: "Antimicrobial & antioxidant preservative" },
  { key: "citric_acid", label: "Citric Acid", unit: "g/dm³", min: 0.0, max: 1.0, step: 0.01, description: "Adds freshness and crisp flavor" },
  { key: "fixed_acidity", label: "Fixed Acidity", unit: "g/dm³", min: 4.0, max: 16.0, step: 0.1, description: "Tartaric acid (structural acidity)" },
  { key: "residual_sugar", label: "Residual Sugar", unit: "g/dm³", min: 0.5, max: 16.0, step: 0.1, description: "Remaining sugar after fermentation" },
  { key: "chlorides", label: "Chlorides", unit: "g/dm³", min: 0.01, max: 0.6, step: 0.001, description: "Salt concentration in the wine" },
  { key: "free_sulfur_dioxide", label: "Free SO₂", unit: "mg/dm³", min: 1.0, max: 72.0, step: 1.0, description: "Free sulfur dioxide molecules" },
  { key: "total_sulfur_dioxide", label: "Total SO₂", unit: "mg/dm³", min: 6.0, max: 289.0, step: 1.0, description: "Free + bound sulfur dioxide" },
  { key: "density", label: "Density", unit: "g/cm³", min: 0.990, max: 1.004, step: 0.0002, description: "Density compared to water" },
  { key: "pH", label: "pH Level", unit: "pH", min: 2.7, max: 4.0, step: 0.01, description: "Acidity vs alkalinity scale" },
];

const PRESETS: Record<string, Record<string, number>> = {
  average: {
    fixed_acidity: 7.4,
    volatile_acidity: 0.7,
    citric_acid: 0.0,
    residual_sugar: 1.9,
    chlorides: 0.076,
    free_sulfur_dioxide: 11.0,
    total_sulfur_dioxide: 34.0,
    density: 0.9978,
    pH: 3.51,
    sulphates: 0.56,
    alcohol: 9.4,
  },
  premium: {
    fixed_acidity: 8.5,
    volatile_acidity: 0.28,
    citric_acid: 0.56,
    residual_sugar: 2.2,
    chlorides: 0.055,
    free_sulfur_dioxide: 18.0,
    total_sulfur_dioxide: 40.0,
    density: 0.9942,
    pH: 3.25,
    sulphates: 0.85,
    alcohol: 12.8,
  },
  lowQuality: {
    fixed_acidity: 6.8,
    volatile_acidity: 1.04,
    citric_acid: 0.02,
    residual_sugar: 2.4,
    chlorides: 0.12,
    free_sulfur_dioxide: 8.0,
    total_sulfur_dioxide: 65.0,
    density: 0.9985,
    pH: 3.65,
    sulphates: 0.45,
    alcohol: 8.8,
  },
};

interface PredictionResult {
  predicted_quality: number;
  rounded_quality: number;
  status: string;
}

export default function Home() {
  const [features, setFeatures] = useState<Record<string, number>>(PRESETS.average);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSliderChange = (key: string, value: number) => {
    setFeatures((prev) => ({ ...prev, [key]: value }));
  };

  const applyPreset = (presetName: string) => {
    if (PRESETS[presetName]) {
      setFeatures(PRESETS[presetName]);
      setPrediction(null);
      setError(null);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    try {
      const response = await fetch(`${apiUrl}/api/v1/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(features),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      const data: PredictionResult = await response.json();
      setPrediction(data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to connect to API";
      setError(
        `${message}. Make sure your FastAPI backend is running on http://localhost:8000!`
      );
    } finally {
      setLoading(false);
    }
  };

  const getQualityBadge = (score: number) => {
    if (score >= 7.0) return { label: "Exceptional / Premium", color: "bg-emerald-500 text-white" };
    if (score >= 6.0) return { label: "Good Quality", color: "bg-blue-500 text-white" };
    if (score >= 5.0) return { label: "Standard / Average", color: "bg-amber-500 text-white" };
    return { label: "Below Average", color: "bg-rose-500 text-white" };
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="border-b border-zinc-800 pb-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3">
                <span className="text-4xl">🍷</span>
                <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-red-500 via-rose-400 to-amber-300 bg-clip-text text-transparent">
                  VinoLens
                </h1>
              </div>
              <p className="text-zinc-400 text-sm mt-1">
                Machine Learning Wine Quality Intelligence Platform
              </p>
            </div>

            {/* Quick Presets */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-semibold mr-1">
                Presets:
              </span>
              <button
                onClick={() => applyPreset("average")}
                className="text-xs px-3 py-1.5 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 transition"
              >
                Table Red (~5.0)
              </button>
              <button
                onClick={() => applyPreset("premium")}
                className="text-xs px-3 py-1.5 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-emerald-500/40 text-emerald-300 transition"
              >
                Premium Aged (~7.0+)
              </button>
              <button
                onClick={() => applyPreset("lowQuality")}
                className="text-xs px-3 py-1.5 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-rose-500/40 text-rose-300 transition"
              >
                High Volatile Acid (~4.8)
              </button>
            </div>
          </div>
        </header>

        {/* Prediction Results Banner */}
        {prediction && (
          <div className="rounded-2xl border border-zinc-800 bg-gradient-to-br from-zinc-900/90 to-zinc-900/40 p-6 shadow-2xl backdrop-blur">
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
              <div className="space-y-2 text-center md:text-left">
                <span className="text-xs uppercase tracking-widest text-zinc-400 font-semibold">
                  ML Model Prediction
                </span>
                <div className="flex items-baseline gap-3">
                  <span className="text-5xl font-black text-white tracking-tight">
                    {prediction.predicted_quality.toFixed(2)}
                  </span>
                  <span className="text-xl text-zinc-500 font-medium">/ 10</span>
                  <span
                    className={`text-xs px-2.5 py-1 rounded-full font-bold uppercase tracking-wider ${
                      getQualityBadge(prediction.predicted_quality).color
                    }`}
                  >
                    {getQualityBadge(prediction.predicted_quality).label}
                  </span>
                </div>
                <p className="text-sm text-zinc-400">
                  Estimated based on 11 physicochemical properties via trained Linear Regression pipeline.
                </p>
              </div>

              {/* Progress visualizer */}
              <div className="w-full md:w-72 space-y-2">
                <div className="flex justify-between text-xs text-zinc-400">
                  <span>Rating Scale</span>
                  <span className="font-semibold text-white">Score {prediction.predicted_quality.toFixed(1)}</span>
                </div>
                <div className="w-full h-3 bg-zinc-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-amber-500 via-rose-500 to-emerald-500 transition-all duration-700"
                    style={{
                      width: `${Math.min(100, Math.max(0, ((prediction.predicted_quality - 3) / 5) * 100))}%`,
                    }}
                  />
                </div>
                <div className="flex justify-between text-[10px] text-zinc-500">
                  <span>3 (Poor)</span>
                  <span>5 (Average)</span>
                  <span>8 (Exceptional)</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error Notification */}
        {error && (
          <div className="rounded-xl border border-rose-500/50 bg-rose-950/30 p-4 text-rose-300 text-sm flex items-start gap-3">
            <span className="text-lg">⚠️</span>
            <div>
              <p className="font-semibold">Unable to fetch prediction</p>
              <p className="text-xs text-rose-300/80 mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Sliders Grid */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-zinc-200">
              Physicochemical Properties ({FEATURES.length} Features)
            </h2>
            <button
              onClick={handlePredict}
              disabled={loading}
              className="px-6 py-2.5 rounded-xl font-medium bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 disabled:opacity-50 text-white shadow-lg shadow-red-900/30 transition transform active:scale-95 cursor-pointer"
            >
              {loading ? "Analyzing Chemistry..." : "Analyze Wine 🚀"}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {FEATURES.map((feat) => {
              const val = features[feat.key] ?? feat.min;
              return (
                <div
                  key={feat.key}
                  className="rounded-xl border border-zinc-800/80 bg-zinc-900/60 p-4 space-y-3 hover:border-zinc-700 transition"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-semibold text-zinc-200 block">
                        {feat.label}
                      </label>
                      <span className="text-[11px] text-zinc-500 line-clamp-1">
                        {feat.description}
                      </span>
                    </div>
                    <span className="text-xs font-mono font-bold bg-zinc-800 text-rose-300 px-2 py-1 rounded border border-zinc-700">
                      {val} {feat.unit}
                    </span>
                  </div>

                  {/* Range Slider */}
                  <input
                    type="range"
                    min={feat.min}
                    max={feat.max}
                    step={feat.step}
                    value={val}
                    onChange={(e) => handleSliderChange(feat.key, parseFloat(e.target.value))}
                    className="w-full accent-rose-500 cursor-pointer h-1.5 bg-zinc-800 rounded-lg appearance-none"
                  />

                  <div className="flex justify-between text-[10px] text-zinc-500 font-mono">
                    <span>{feat.min}</span>
                    <span>{feat.max}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Footer info */}
        <footer className="pt-6 border-t border-zinc-900 text-center text-xs text-zinc-600">
          VinoLens &bull; Built with FastAPI &bull; Next.js 15 &bull; Scikit-Learn
        </footer>
      </div>
    </div>
  );
}
