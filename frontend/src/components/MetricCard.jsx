function MetricCard({
  title,
  value,
  subtitle,
}) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 hover:border-zinc-700 transition-all duration-300 hover:-translate-y-1">

      <p className="text-zinc-400 text-lg mb-4">
        {title}
      </p>

      <h2 className="text-5xl font-bold text-white mb-4 break-words">
        {value}
      </h2>

      {subtitle && (
        <p className="text-zinc-500">
          {subtitle}
        </p>
      )}

    </div>
  );
}

export default MetricCard;