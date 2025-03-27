import { useState } from "react";
import PatientInputForm from "./components/PatientInputForm";
import PatientMedicalHistory from "./components/PatientMedicalHistory";
import TriageResult from "./components/TriageResult";
import OverrideTriage from "./components/OverrideTriage";
import SubmitButton from "./components/SubmitButton";

const App: React.FC = () => {
  const [patientInfo, setPatientInfo] = useState<{ conditions: string; medications: string } | null>(null);
  const [triageScore, setTriageScore] = useState("");
  const [triageExplanation, setTriageExplanation] = useState("");
  const [showResults, setShowResults] = useState(false);
  const [inputKey, setInputKey] = useState(0);

  const handleTriageCalculation = (data: any) => {
    // Simulated API calls for fetching medical history and triage score
    const fetchedPatientInfo = { conditions: "Hypertension, Deez, Deez asdjdhwaodhaidhwaiodhwai", medications: "Aspirin" }; // Placeholder
    const calculatedScore = "3";
    const explanation = "AHHHHHHHHHH OHNOOOOOOO";
    
    setPatientInfo(fetchedPatientInfo);
    setTriageScore(calculatedScore);
    setTriageExplanation(explanation);
    setShowResults(true);
  };

  const handleOverride = (newScore: string) => {
    setTriageScore(newScore);
  };

  const handleSubmit = () => {
    alert("Triage decision submitted!");
    setPatientInfo(null);
    setTriageScore("");
    setTriageExplanation("");
    setShowResults(false);
    setInputKey(prevKey => prevKey + 1); // Reset form by changing key
  };

  return (
    <div className="max-w-6xl mx-auto p-6 h-screen flex flex-col justify-center items-center">
      <h1 className="text-2xl font-bold mb-4">ER Triage Assistant</h1>
      <div className={`flex ${showResults ? 'flex-row' : 'flex-col'} w-full justify-center items-center gap-8`}>
        <div className="w-1/2 flex flex-col gap-4">
          <PatientInputForm key={inputKey} onSubmit={handleTriageCalculation} />
          <button
            onClick={() => handleTriageCalculation({})}
            className="mt-4 p-2 bg-blue-500 text-white rounded-md w-full"
          >
            Calculate Triage Score
          </button>
          {showResults && <PatientMedicalHistory data={patientInfo} />}
        </div>
        {showResults && (
          <div className="w-1/2 flex flex-col gap-4">
            <TriageResult score={"Level " + triageScore} explanation={triageExplanation} />
            <OverrideTriage onOverride={handleOverride} />
            <SubmitButton onSubmit={handleSubmit} />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;