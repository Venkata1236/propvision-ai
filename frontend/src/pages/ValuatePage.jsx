import Navbar from "../components/Navbar";
import PropertyForm from "../components/PropertyForm";

function ValuatePage() {
  return (
    <div className="min-h-screen bg-black text-white">

      <Navbar />

      {/* HERO */}

      <section className="max-w-7xl mx-auto px-6 pt-20 pb-10">

        <div className="max-w-4xl">

          <div className="inline-flex items-center gap-2 bg-zinc-900 border border-zinc-800 rounded-full px-5 py-2 mb-8">
            <span className="text-green-400">
              ●
            </span>

            <span className="text-zinc-300">
              AI-Powered Real Estate Intelligence
            </span>
          </div>

          <h1 className="text-6xl md:text-7xl font-bold leading-tight mb-8">
            Next-Generation
            <br />

            Property Valuation
            <br />

            Platform
          </h1>

          <p className="text-zinc-400 text-xl leading-relaxed max-w-3xl">
            PropVision AI combines
            stacking machine learning,
            SHAP explainability,
            RAG-powered comparable
            retrieval, and CrewAI
            agents to deliver
            intelligent property
            valuation insights.
          </p>

        </div>
      </section>

      {/* FORM */}

      <section className="px-6 pb-24">
        <PropertyForm />
      </section>

    </div>
  );
}

export default ValuatePage;