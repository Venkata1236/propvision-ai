import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import ValuatePage from "./pages/ValuatePage";

import ResultsPage from "./pages/ResultsPage";
import HistoryPage from "./pages/HistoryPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<ValuatePage />}
        />

        <Route
          path="/results"
          element={<ResultsPage />}
        />

        <Route
          path="/history"
          element={<HistoryPage />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;