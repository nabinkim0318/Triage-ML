// Override triage level

import { useState } from "react";

interface OverrideTriageProps {
  onOverride: (newScore: string) => void;
}

const OverrideTriage: React.FC<OverrideTriageProps> = ({ onOverride }) => {
  const [overrideScore, setOverrideScore] = useState("");
  const [error, setError] = useState("");

  const handleOverride = () => {
    const score = parseInt(overrideScore, 10);
    if (isNaN(score) || score < 1 || score > 5) {
      setError("Please enter a valid triage level between 1 and 5.");
      return;
    }
    setError(""); // Clear error if input is valid
    onOverride(overrideScore);
  };

  return (
    <div className="p-4 border rounded-md mt-4">
      <h2 className="text-lg font-semibold">Override Triage Level</h2>
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Enter new triage level"
          value={overrideScore}
          onChange={(e) => setOverrideScore(e.target.value)}
          className="p-2 border rounded-md w-3/4 mt-2"
        />
        <button
          onClick={handleOverride}
          className="mt-2 p-2 bg-red-500 text-white rounded-md w-1/4"
        >
          Override
        </button>
      </div>
      {error && <p className="text-sm text-red-500 mt-1">{error}</p>}
    </div>
  );
};

export default OverrideTriage;
