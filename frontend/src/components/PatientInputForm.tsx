import { useState } from "react";

interface PatientInputProps {
  onSubmit: (data: any) => void;
}

const PatientInputForm: React.FC<PatientInputProps> = ({ onSubmit }) => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [dob, setDob] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [vitals, setVitals] = useState({
    bloodPressureSystolic: "",
    bloodPressureDiastolic: "",
    heartRate: "",
    temperature: "",
    respiratoryRate: "",
    oxygenSaturation: "",
  });

  const temperatureUnits = ["°F", "°C"];

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit({ firstName, lastName, dob, symptoms, vitals });
      }}
      className="p-4 border rounded-md w-full"
    >
      <div className="grid grid-cols-2 gap-2 mt-2">
        <input
          type="text"
          placeholder="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          className="p-2 border rounded-md w-full"
        />
        <input
          type="text"
          placeholder="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          className="p-2 border rounded-md w-full"
        />
      </div>
      <input
        type="date"
        placeholder="Date of Birth"
        value={dob}
        onChange={(e) => setDob(e.target.value)}
        className="p-2 border rounded-md w-full mt-2"
      />
      <textarea
        placeholder="Symptoms"
        value={symptoms}
        onChange={(e) => setSymptoms(e.target.value)}
        className="p-2 border rounded-md w-full mt-2"
      />
      <div className="grid grid-cols-2 gap-2 mt-4">
        <input
          type="text"
          placeholder="BP: Systolic (mm Hg)"
          value={vitals.bloodPressureSystolic}
          onChange={(e) => setVitals({ ...vitals, bloodPressureSystolic: e.target.value })}
          className="p-2 border rounded-md w-full"
        />
        <input
          type="text"
          placeholder="BP: Diastolic (mm Hg)"
          value={vitals.bloodPressureDiastolic}
          onChange={(e) => setVitals({ ...vitals, bloodPressureDiastolic: e.target.value })}
          className="p-2 border rounded-md w-full"
        />
      </div>

      <div className="grid grid-cols-1 gap-2 mt-2">
        <input
          type="text"
          placeholder="Heart Rate (bpm)"
          value={vitals.heartRate}
          onChange={(e) => setVitals({ ...vitals, heartRate: e.target.value })}
          className="p-2 border rounded-md w-full"
        />
        <div className="flex gap-2 items-center">
          <input
            type="text"
            placeholder="Temperature"
            value={vitals.temperature}
            onChange={(e) => setVitals({ ...vitals, temperature: e.target.value })}
            className="p-2 border rounded-md w-full"
          />
          <select className="p-2 border rounded-md">
            {temperatureUnits.map((unit) => (
              <option key={unit} value={unit}>{unit}</option>
            ))}
          </select>
        </div>
        <input
          type="text"
          placeholder="Respiratory Rate (breaths/min)"
          value={vitals.respiratoryRate}
          onChange={(e) => setVitals({ ...vitals, respiratoryRate: e.target.value })}
          className="p-2 border rounded-md w-full"
        />
        <input
          type="text"
          placeholder="Oxygen Saturation (%)"
          value={vitals.oxygenSaturation}
          onChange={(e) => setVitals({ ...vitals, oxygenSaturation: e.target.value })}
          className="p-2 border rounded-md w-full"
        />
      </div>
      <button
        type="submit"
        className="mt-4 p-2 bg-blue-500 text-white rounded-md w-full"
      >
        Calculate Triage Score
      </button>
    </form>
  );
};

export default PatientInputForm;
