function LoadingScreen() {

  const steps = [
    "Analyzing property features",
    "Running stacking ensemble",
    "Generating SHAP explanations",
    "Retrieving comparable sales",
    "Generating AI insights",
  ];

  return (
    <div className="fixed inset-0 bg-black/95 backdrop-blur-xl z-[100] flex items-center justify-center px-6">

      <div className="max-w-2xl w-full">

        {/* LOGO */}

        <div className="text-center mb-14">

          <div className="w-28 h-28 rounded-full border-4 border-zinc-800 border-t-white animate-spin mx-auto mb-8" />

          <h1 className="text-5xl font-bold text-white mb-4">
            PropVision AI
          </h1>

          <p className="text-zinc-400 text-xl">
            AI valuation engine processing...
          </p>

        </div>

        {/* STEPS */}

        <div className="space-y-5">

          {steps.map((step, index) => (
            <div
              key={index}
              className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 flex items-center gap-5 animate-pulse"
            >

              <div className="w-4 h-4 rounded-full bg-green-400" />

              <p className="text-zinc-300 text-lg">
                {step}
              </p>

            </div>
          ))}

        </div>

      </div>
    </div>
  );
}

export default LoadingScreen;