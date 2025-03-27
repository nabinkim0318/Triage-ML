// Enter in patient name, DOB, vitals, and symptoms to submit

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
    bloodPressure: "",
    heartRate: "",
    temperature: "",
    respiratoryRate: "",
    oxygenSaturation: "",
  });

  return (
    <div className="p-4 border rounded-md w-full">
      
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
      <div className="grid grid-cols-2 gap-2 mt-2">
        {Object.keys(vitals).map((key) => (
          <input
            key={key}
            type="text"
            placeholder={key.replace(/([A-Z])/g, ' $1')}
            value={(vitals as any)[key]}
            onChange={(e) => setVitals({ ...vitals, [key]: e.target.value })}
            className="p-2 border rounded-md"
          />
        ))}
      </div>
    </div>
  );
};

export default PatientInputForm;