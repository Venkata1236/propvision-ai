import { useLocation } from "react-router-dom";

import VerdictBadge from "../components/VerdictBadge";
import ConfidenceBar from "../components/ConfidenceBar";
import SHAPExplanation from "../components/SHAPExplanation";
import MetricCard from "../components/MetricCard";

function ResultsPage() {
  const location = useLocation();

  const data = location.state;

  if (!data) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center text-3xl">
        No valuation data found
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white px-6 py-16">
      <div className="max-w-7xl mx-auto">

        {/* HEADER */}

        <div className="mb-12">
          <h1 className="text-5xl font-bold mb-4">
            AI Valuation Results
          </h1>

          <p className="text-zinc-400 text-lg">
            AI-powered property intelligence report
          </p>
        </div>

        {/* HERO CARD */}

        <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-10 mb-10">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-8">

            <div>
              <p className="text-zinc-400 mb-2">
                Predicted Property Value
              </p>

              <h2 className="text-6xl font-bold text-white">
                ₹
                {Number(
                  data.predicted_price_inr
                ).toLocaleString()}
              </h2>
            </div>

            <div className="bg-zinc-800 rounded-2xl px-8 py-6">
              <p className="text-zinc-400 mb-2">
                Confidence Level
              </p>

              <h3 className="text-3xl font-bold">
                {
                  data.confidence_range
                    ?.confidence_level
                }
              </h3>
            </div>

          </div>
        </div>

        {/* CONFIDENCE ANALYSIS */}

        <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 mb-10">

          <h2 className="text-3xl font-bold mb-8">
            Confidence Analysis
          </h2>

          <ConfidenceBar
            low={
              data.confidence_range
                ?.low_inr
            }
            predicted={
              data.predicted_price_inr
            }
            high={
              data.confidence_range
                ?.high_inr
            }
          />

        </div>

        {/* SHAP FACTORS */}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 mb-10">

          {/* POSITIVE */}

          <div className="bg-zinc-900 border border-green-900 rounded-3xl p-8">
            <h2 className="text-3xl font-bold mb-8 text-green-400">
              Positive Factors
            </h2>

            <div className="space-y-6">

              {data.shap_explanation?.positive_factors?.map(
                (factor, index) => (
                  <div
                    key={index}
                    className="bg-zinc-800 rounded-2xl p-5"
                  >
                    <h3 className="text-xl font-semibold mb-2">
                      {factor.factor}
                    </h3>

                    <p className="text-zinc-400 mb-3">
                      {
                        factor.plain_english
                      }
                    </p>

                    <p className="text-green-400 font-bold">
                      + ₹
                      {Number(
                        factor.impact_inr
                      ).toLocaleString()}
                    </p>
                  </div>
                )
              )}

            </div>
          </div>

          {/* NEGATIVE */}

          <div className="bg-zinc-900 border border-red-900 rounded-3xl p-8">
            <h2 className="text-3xl font-bold mb-8 text-red-400">
              Negative Factors
            </h2>

            <div className="space-y-6">

              {data.shap_explanation?.negative_factors?.map(
                (factor, index) => (
                  <div
                    key={index}
                    className="bg-zinc-800 rounded-2xl p-5"
                  >
                    <h3 className="text-xl font-semibold mb-2">
                      {factor.factor}
                    </h3>

                    <p className="text-zinc-400 mb-3">
                      {
                        factor.plain_english
                      }
                    </p>

                    <p className="text-red-400 font-bold">
                      - ₹
                      {Number(
                        factor.impact_inr
                      ).toLocaleString()}
                    </p>
                  </div>
                )
              )}

            </div>
          </div>

        </div>

        {/* SHAP VISUALIZATION */}

        <SHAPExplanation
          positiveFactors={
            data.shap_explanation
              ?.positive_factors || []
          }
          negativeFactors={
            data.shap_explanation
              ?.negative_factors || []
          }
        />

        {/* COMPARABLE SALES */}

        <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 mb-10">

          <h2 className="text-3xl font-bold mb-8">
            Comparable Sales
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

            {data.comparable_sales?.map(
              (property, index) => (
                <div
                  key={index}
                  className="bg-zinc-800 rounded-2xl p-6"
                >
                  <h3 className="text-xl font-semibold mb-4">
                    {
                      property.description
                    }
                  </h3>

                  <div className="space-y-3 text-zinc-400">

                    <div className="flex justify-between">
                      <span>
                        Sale Price
                      </span>

                      <span className="text-white font-semibold">
                        ₹
                        {Number(
                          property.sale_price_inr
                        ).toLocaleString()}
                      </span>
                    </div>

                    <div className="flex justify-between">
                      <span>
                        Similarity
                      </span>

                      <span className="text-green-400">
                        {(
                          property.similarity_score *
                          100
                        ).toFixed(1)}
                        %
                      </span>
                    </div>

                    <div className="flex justify-between">
                      <span>
                        Neighborhood
                      </span>

                      <span className="text-white">
                        {
                          property.neighborhood
                        }
                      </span>
                    </div>

                  </div>
                </div>
              )
            )}

          </div>
        </div>

        {/* INVESTMENT RECOMMENDATION */}

        <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 mb-10">

          <h2 className="text-3xl font-bold mb-8">
            Investment Recommendation
          </h2>

          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-8">

            <div>

              <p className="text-zinc-400 mb-4">
                AI Verdict
              </p>

              <VerdictBadge
                verdict={
                  data
                    .investment_recommendation
                    ?.verdict || "BUY"
                }
              />

            </div>

            <div className="max-w-3xl">

              <p className="text-zinc-300 leading-relaxed text-lg">
                {
                  data
                    .investment_recommendation
                    ?.reasoning
                }
              </p>

            </div>

          </div>

        </div>

        {/* MARKET INSIGHTS */}

        <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8">

          <h2 className="text-3xl font-bold mb-8">
            AI Market Insights
          </h2>

          <div className="space-y-6">

            {data.market_insights?.map(
              (insight, index) => (
                <div
                  key={index}
                  className="bg-zinc-800 rounded-2xl p-6"
                >
                  <p className="text-zinc-200 leading-relaxed">
                    {insight}
                  </p>
                </div>
              )
            )}

          </div>

        </div>

      </div>
    </div>
  );
}

export default ResultsPage;