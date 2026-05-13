function ConfidenceBar({
  low,
  predicted,
  high,
}) {

  const range = high - low;

  const position =
    ((predicted - low) /
      range) *
    100;

  return (
    <div className="w-full">

      <div className="flex justify-between text-sm text-zinc-500 mb-3">
        <span>
          ₹
          {Number(
            low
          ).toLocaleString()}
        </span>

        <span>
          ₹
          {Number(
            high
          ).toLocaleString()}
        </span>
      </div>

      <div className="relative h-5 bg-zinc-800 rounded-full overflow-hidden">

        <div className="absolute inset-0 bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 opacity-70" />

        <div
          className="absolute top-1/2 -translate-y-1/2 w-6 h-6 bg-white rounded-full border-4 border-black shadow-xl"
          style={{
            left: `${position}%`,
            transform:
              "translate(-50%, -50%)",
          }}
        />

      </div>

      <div className="text-center mt-4">
        <p className="text-zinc-400">
          Predicted Market Value
        </p>

        <h3 className="text-3xl font-bold mt-2">
          ₹
          {Number(
            predicted
          ).toLocaleString()}
        </h3>
      </div>

    </div>
  );
}

export default ConfidenceBar;