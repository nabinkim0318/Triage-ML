import { useState, useEffect } from "react";
import PatientInputForm from "./components/PatientInputForm";
import PatientMedicalHistory from "./components/PatientMedicalHistory";
import TriageResult from "./components/TriageResult";
import OverrideTriage from "./components/OverrideTriage";
import SubmitButton from "./components/SubmitButton";

import { fetchMedicalHistory } from "./api/fetchMedicalHistory";

const App: React.FC = () => {
  const [patientInfo, setPatientInfo] = useState<{ conditions: string; medications: string } | null>(null);
  const [triageScore, setTriageScore] = useState("");
  const [originalTriageScore, setOriginalTriageScore] = useState<string | null>(null);
  const [triageExplanation, setTriageExplanation] = useState("");
  const [showResults, setShowResults] = useState(false);
  const [inputKey, setInputKey] = useState(0);
  const [loading, setLoading] = useState(false);
  const [dots, setDots] = useState(".");

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setDots((prev) => (prev === "." ? ".." : prev === ".." ? "..." : "."));
      }, 500); // Change every 500ms
      return () => clearInterval(interval); // Cleanup on unmount or when loading stops
    }
  }, [loading]);

  const handleTriageCalculation = async (data: any) => {
    setLoading(true);

    const requestBody = {
      firstName: data.firstName,
      lastName: data.lastName,
      dob: data.dob,
      symptoms: data.symptoms,
      vitals: {
        heartRate: data.vitals.heartRate,
        bloodPressureSystolic: data.vitals.bloodPressureSystolic,
        bloodPressureDiastolic: data.vitals.bloodPressureDiastolic,
        temperature: data.vitals.temperature,
        temperatureUnit: data.vitals.temperatureUnit,
        respiratoryRate: data.vitals.respiratoryRate,
        oxygenSaturation: data.vitals.oxygenSaturation,
      },
    };

    try {
      const response = await fetchMedicalHistory(requestBody);
      const { triage_score, triage_explanation, ...patientData } = response;
      setPatientInfo(patientData);
      setTriageScore(triage_score);
      setOriginalTriageScore(triage_score);
      setTriageExplanation(triage_explanation);
      setShowResults(true);
    } catch (error) {
      console.error("Error fetching medical history or calculating triage:", error);
      alert("Failed to calculate triage score. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleOverride = (newScore: string) => {
    setTriageScore(newScore);
  };

  const handleSubmit = () => {
    alert("Triage decision submitted!");
    setPatientInfo(null);
    setTriageScore("");
    setOriginalTriageScore(null);
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
          <div className="h-6">
            {loading && <p className="text-sm font-semibold">Calculating score{dots}</p>}
          </div>
        </div>
        {showResults && (
          <div className="w-3/5 flex flex-col relative">
            <PatientMedicalHistory data={patientInfo} />
            <TriageResult
              score={"Level " + triageScore}
              explanation={triageExplanation}
              isOverridden={originalTriageScore !== triageScore} // Pass true if old score exists
              originalScore={originalTriageScore ? "Level " + originalTriageScore : undefined} // Pass old score if it exists
            />
            <OverrideTriage onOverride={handleOverride} />
            <SubmitButton onSubmit={handleSubmit} />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;