// Override triage level

import { useState } from "react";

interface OverrideTriageProps {
  onOverride: (newScore: string) => void;
}

const OverrideTriage: React.FC<OverrideTriageProps> = ({ onOverride }) => {
  const [overrideScore, setOverrideScore] = useState("");

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
          onClick={() => onOverride(overrideScore)}
          className="mt-2 p-2 bg-red-500 text-white rounded-md w-1/4"
        >
          Override
        </button>
      </div>
      
    </div>
  );
};

export default OverrideTriage;
