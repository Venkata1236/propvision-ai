import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="w-full border-b border-zinc-800 bg-black/80 backdrop-blur-xl sticky top-0 z-50">

      <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">

        {/* LOGO */}

        <Link
          to="/"
          className="text-3xl font-bold text-white"
        >
          PropVision AI
        </Link>

        {/* NAVIGATION */}

        <div className="flex items-center gap-8">

          <Link
            to="/"
            className="text-zinc-400 hover:text-white transition-colors"
          >
            Home
          </Link>

          <Link
            to="/history"
            className="text-zinc-400 hover:text-white transition-colors"
          >
            History
          </Link>

          <a
            href="https://github.com/Venkata1236/propvision-ai"
            target="_blank"
            rel="noreferrer"
            className="bg-white text-black px-5 py-2 rounded-xl font-semibold hover:bg-zinc-200 transition-all"
          >
            GitHub
          </a>

        </div>
      </div>
    </nav>
  );
}

export default Navbar;