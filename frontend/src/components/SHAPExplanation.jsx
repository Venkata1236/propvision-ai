import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function SHAPWaterfallChart({
  positiveFactors,
  negativeFactors,
}) {

  const positiveData =
    positiveFactors.map(
      (factor) => ({
        name:
          factor.factor.substring(
            0,
            18
          ),
        impact:
          factor.impact_inr,
      })
    );

    
  const negativeData =
    negativeFactors.map(
      (factor) => ({
        name:
          factor.factor.substring(
            0,
            18
          ),
        impact:
          -factor.impact_inr,
      })
    );

  const chartData = [
    ...positiveData,
    ...negativeData,
  ];

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 mb-10">

      <h2 className="text-3xl font-bold mb-8">
        SHAP Explainability Analysis
      </h2>

      <div className="h-[450px]">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <BarChart
            data={chartData}
          >

            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#27272a"
            />

            <XAxis
              dataKey="name"
              stroke="#a1a1aa"
            />

            <YAxis
              stroke="#a1a1aa"
            />

            <Tooltip
              contentStyle={{
                backgroundColor:
                  "#18181b",
                border:
                  "1px solid #27272a",
                borderRadius:
                  "16px",
              }}
            />

            <Bar
              dataKey="impact"
              radius={[12, 12, 0, 0]}
            />

          </BarChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default SHAPWaterfallChart;