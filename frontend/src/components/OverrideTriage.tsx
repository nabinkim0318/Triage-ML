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
      <input
        type="text"
        placeholder="Enter new triage level"
        value={overrideScore}
        onChange={(e) => setOverrideScore(e.target.value)}
        className="p-2 border rounded-md w-full mt-2"
      />
      <button
        onClick={() => onOverride(overrideScore)}
        className="mt-2 p-2 bg-red-500 text-white rounded-md w-full"
      >
        Override
      </button>
    </div>
  );
};

export default OverrideTriage;
