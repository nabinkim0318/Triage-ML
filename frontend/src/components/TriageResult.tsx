// Displays triage score and give explanation from LLM

interface TriageResultProps {
    score: string;
    explanation: string;
  }
  
  const TriageResult: React.FC<TriageResultProps> = ({ score, explanation }) => {
    return (
      <div className="p-4 border rounded-md mt-4">
        <h2 className="text-lg font-semibold">Triage Score</h2>
        <p className="text-xl font-bold">{score}</p>
        <p className="mt-2 text-sm">
          <span className="font-bold">Reasoning: </span>{explanation}</p>
      </div>
    );
  };
  
  export default TriageResult;