import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { valuateProperty } from "../services/api";

function PropertyForm() {
  const navigate = useNavigate();

  const [loading, setLoading] =
    useState(false);

  const [formData, setFormData] =
    useState({
      neighborhood: "NoRidge",
      total_sqft: 2400,
      bedrooms: 4,
      bathrooms: 3,
      overall_quality: 8,
      house_age_years: 5,
      is_remodeled: true,
      has_garage: true,
      has_pool: false,
      floor_number: 2,
    });

  const handleChange = (e) => {
    const {
      name,
      value,
      type,
      checked,
    } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    }));
  };

  const handleSubmit = async (
    e
  ) => {
    e.preventDefault();

    try {
      setLoading(true);

      const response =
        await valuateProperty(
          formData
        );

      navigate("/results", {
        state: response,
      });
    } catch (error) {
      console.error(error);

      alert(
        "Valuation failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto bg-zinc-900 border border-zinc-800 rounded-3xl p-10 shadow-2xl">
      <div className="mb-10">
        <h1 className="text-5xl font-bold text-white mb-4">
          PropVision AI
        </h1>

        <p className="text-zinc-400 text-lg">
          AI-powered property
          valuation and market
          intelligence
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-8"
      >
        {/* ROW 1 */}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-zinc-300 mb-2">
              Neighborhood
            </label>

            <input
              type="text"
              name="neighborhood"
              value={
                formData.neighborhood
              }
              onChange={
                handleChange
              }
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="block text-zinc-300 mb-2">
              Total Area (sqft)
            </label>

            <input
              type="number"
              name="total_sqft"
              value={
                formData.total_sqft
              }
              onChange={
                handleChange
              }
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="block text-zinc-300 mb-2">
              Floor Number
            </label>

            <input
              type="number"
              name="floor_number"
              value={
                formData.floor_number
              }
              onChange={
                handleChange
              }
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white"
            />
          </div>
        </div>

        {/* ROW 2 */}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-zinc-300 mb-2">
              Bedrooms
            </label>

            <input
              type="number"
              name="bedrooms"
              value={
                formData.bedrooms
              }
              onChange={
                handleChange
              }
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="block text-zinc-300 mb-2">
              Bathrooms
            </label>

            <input
              type="number"
              name="bathrooms"
              value={
                formData.bathrooms
              }
              onChange={
                handleChange
              }
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white"
            />
          </div>

          <div>
            <label className="block text-zinc-300 mb-2">
              Overall Quality
            </label>

            <input
              type="range"
              min="1"
              max="10"
              name="overall_quality"
              value={
                formData.overall_quality
              }
              onChange={
                handleChange
              }
              className="w-full"
            />

            <div className="flex justify-between text-sm text-zinc-500 mt-2">
              <span>Poor</span>
              <span>
                {
                  formData.overall_quality
                }
                /10
              </span>
              <span>
                Excellent
              </span>
            </div>
          </div>
        </div>

        {/* ROW 3 */}

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <label className="block text-zinc-300 mb-2">
              House Age
            </label>

            <input
              type="number"
              name="house_age_years"
              value={
                formData.house_age_years
              }
              onChange={
                handleChange
              }
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white"
            />
          </div>

          <label className="flex items-center gap-3 text-zinc-300">
            <input
              type="checkbox"
              name="is_remodeled"
              checked={
                formData.is_remodeled
              }
              onChange={
                handleChange
              }
            />

            Remodeled
          </label>

          <label className="flex items-center gap-3 text-zinc-300">
            <input
              type="checkbox"
              name="has_garage"
              checked={
                formData.has_garage
              }
              onChange={
                handleChange
              }
            />

            Garage
          </label>

          <label className="flex items-center gap-3 text-zinc-300">
            <input
              type="checkbox"
              name="has_pool"
              checked={
                formData.has_pool
              }
              onChange={
                handleChange
              }
            />

            Pool
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-white text-black py-4 rounded-2xl font-bold text-lg hover:bg-zinc-200 transition-all"
        >
          {loading
            ? "Analyzing Property..."
            : "Get AI Valuation"}
        </button>
      </form>
    </div>
  );
}

export default PropertyForm;