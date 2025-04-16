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
    temperatureUnit: "F",
    respiratoryRate: "",
    oxygenSaturation: "",
  });

  const [errors, setErrors] = useState<{ firstName?: string; lastName?: string; dob?: string }>({});

  const validateFields = () => {
    const newErrors: { firstName?: string; lastName?: string; dob?: string } = {};
    if (!firstName.trim()) newErrors.firstName = "First name is required.";
    if (!lastName.trim()) newErrors.lastName = "Last name is required.";
    if (!dob.trim()) newErrors.dob = "Date of birth is required.";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0; // Return true if no errors
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateFields()) {
      onSubmit({ firstName, lastName, dob, symptoms, vitals });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded-md w-full">
      <div className="grid grid-cols-2 gap-2 mt-2">
        <div>
          <input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="p-2 border rounded-md w-full"
          />
          {errors.firstName && <p className="text-sm text-red-500">{errors.firstName}</p>}
        </div>
        <div>
          <input
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            className="p-2 border rounded-md w-full"
          />
          {errors.lastName && <p className="text-sm text-red-500">{errors.lastName}</p>}
        </div>
      </div>
      <div className="mt-2">
        <input
          type="date"
          placeholder="Date of Birth"
          value={dob}
          onChange={(e) => setDob(e.target.value)}
          className="p-2 border rounded-md w-full"
        />
        {errors.dob && <p className="text-sm text-red-500">{errors.dob}</p>}
      </div>
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
          <select
            value={vitals.temperatureUnit}
            onChange={(e) => setVitals({ ...vitals, temperatureUnit: e.target.value })}
            className="p-2 border rounded-md"
          >
            <option value="F">°F</option>
            <option value="C">°C</option>
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