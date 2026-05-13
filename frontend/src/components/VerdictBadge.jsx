function VerdictBadge({
  verdict,
}) {

  const styles = {
    BUY: "bg-green-500/20 text-green-400 border-green-500/30",

    WAIT: "bg-orange-500/20 text-orange-400 border-orange-500/30",

    NEGOTIATE:
      "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  };

  return (
    <div
      className={`inline-flex items-center justify-center px-8 py-4 rounded-2xl border text-2xl font-bold ${styles[verdict]}`}
    >
      {verdict}
    </div>
  );
}

export default VerdictBadge;