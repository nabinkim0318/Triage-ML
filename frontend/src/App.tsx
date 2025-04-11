import { useState } from "react";
import PatientInputForm from "./components/PatientInputForm";
import PatientMedicalHistory from "./components/PatientMedicalHistory";
import TriageResult from "./components/TriageResult";
import OverrideTriage from "./components/OverrideTriage";
import SubmitButton from "./components/SubmitButton";

import { fetchMedicalHistory } from "./api/fetchMedicalHistory";

const App: React.FC = () => {
  const [patientInfo, setPatientInfo] = useState<{ conditions: string; medications: string } | null>(null);
  const [triageScore, setTriageScore] = useState("");
  const [triageExplanation, setTriageExplanation] = useState("");
  const [showResults, setShowResults] = useState(false);
  const [inputKey, setInputKey] = useState(0);

  const handleTriageCalculation = async (data: any) => {
    const fetchedPatientInfo = await fetchMedicalHistory(data.firstName, data.lastName, data.dob);

    const calculatedScore = "2";
    const explanation = "Patient assigned ESI Level 2 due to chest pain, shortness of breath, and a history of myocardial infarction and hypertension—indicating high cardiac risk. Immediate attention recommended despite stable vitals to prevent deterioration.";
    
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
    setInputKey(prevKey => prevKey + 1);
  };

  return (
    <div className="max-w-7xl mx-auto p-6 h-screen flex flex-col justify-center items-center">
      <div className={`flex ${showResults ? 'flex-row' : 'flex-col'} w-full justify-center items-center gap-8`}>
        <div className="w-2/5 flex flex-col gap-4 items-center">
          <h1 className="text-2xl font-bold mb-4">ER Triage Assistant</h1>
          <PatientInputForm key={inputKey} onSubmit={handleTriageCalculation} />
        </div>
        {showResults && (
          <div className="w-3/5 flex flex-col">
            <PatientMedicalHistory data={patientInfo} />
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