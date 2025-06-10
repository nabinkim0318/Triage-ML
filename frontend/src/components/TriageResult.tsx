// Displays triage score and give explanation from LLM

interface TriageResultProps {
    score: string;
    explanation: string;
    isOverridden?: boolean;
    originalScore?: string;
  }
  
  const TriageResult: React.FC<TriageResultProps> = ({ score, explanation, isOverridden, originalScore }) => {
    isOverridden = originalScore !== score;

    return (
      <div className="p-4 border rounded-md mt-4">
        <div className="flex items-center">
          <h2 className="text-xl font-bold">{score}</h2>
          {isOverridden && <span className="text-sm font-semibold text-red-500 ml-1">(Overridden)</span>}
        </div>
        {isOverridden && originalScore && (
          <p className="text-xs text-gray-500">(Original score: {originalScore})</p>
        )}
        <p className="text-sm mt-2">{explanation}</p>
      </div>
    );
  };
  
  export default TriageResult;