import React from "react";

interface PatientMedicalHistoryProps {
  data: any; // Replace `any` with a proper type if available
}

const PatientMedicalHistory: React.FC<PatientMedicalHistoryProps> = ({ data }) => {
  if (!data) {
    return null;
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return "Unknown";
    const date = new Date(dateString);
    return date.toISOString().split("T")[0]; // Extract YYYY-MM-DD
  };

  const hasMedicalHistory =
    data.conditions?.conditions?.length > 0 ||
    data.medications?.medications?.length > 0 ||
    data.allergies?.allergies?.length > 0 ||
    data.clinical_notes?.notes?.length > 0 ||
    data.encounters?.encounters?.length > 0;

  return (
    <div className="p-4 border rounded-md mt-4 overflow-auto max-h-80 w-full">
      <h2 className="text-lg font-bold">Patient Medical Information</h2>

      {/* Basic Patient Information */}
      <div className="mb-4">
        <p><strong>Name:</strong> {data.name || "N/A"}</p>
        <p><strong>Date of Birth:</strong> {data.birthDate || "N/A"}</p>
        <p><strong>Age:</strong> {data.age || "N/A"}</p>
        <p><strong>Gender:</strong> {data.gender || "N/A"}</p>
      </div>

      {hasMedicalHistory ? (
        <>
          <div className="mb-4">
            <h3 className="font-bold">Conditions</h3>
            {data.conditions?.conditions?.length > 0 ? (
              <ul className="list-disc ml-6 text-sm">
                {data.conditions.conditions.map((condition: any, index: number) => (
                  <li key={index}>{condition.code.text || "Unknown Condition"}</li>
                ))}
              </ul>
            ) : (
              <p className="text-sm">No conditions found.</p>
            )}
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Medications</h3>
            {data.medications?.medications?.length > 0 ? (
              <ul className="list-disc ml-6 text-sm">
                {data.medications.medications.map((med: any, index: number) => (
                  <li key={index}>
                    <p>{med.medication.text || "Unknown Medication"}</p>
                    {med.dosage?.length > 0 && (
                      <ul className="list-disc ml-6">
                        {med.dosage.map((dose: any, doseIndex: number) => (
                          <li key={doseIndex}>{dose.text || "Unknown Dosage"}</li>
                        ))}
                      </ul>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm">No medications found.</p>
            )}
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Allergies</h3>
            {data.allergies?.allergies?.length > 0 ? (
              <ul className="list-disc ml-6 text-sm">
                {data.allergies.allergies.map((allergy: any, index: number) => (
                  <li key={index}>
                    <p>{allergy.name || "Unknown Allergy"}</p> - {allergy.criticality || "Unknown Criticality"}
                    {allergy.reaction?.length > 0 && (
                      <ul className="list-disc ml-6">
                        {allergy.reaction.map((reaction: any, reactionIndex: number) => (
                          <li key={reactionIndex}>{reaction.manifestation?.[0] || "Unknown Reaction"}</li>
                        ))}
                      </ul>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm">No allergies found.</p>
            )}
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Clinical Notes</h3>
            {data.clinical_notes?.notes?.length > 0 ? (
              <ul className="list-disc ml-6 text-sm">
                {data.clinical_notes.notes.map((note: any, index: number) => (
                  <li key={index}>
                    <p>{note.type || "Unknown Note Type"}</p> ({note.date || "Unknown Date"}): {note.content || "No Content"}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm">No clinical notes found.</p>
            )}
          </div>

          <div className="mt-2">
            <h3 className="font-bold">Past Encounters</h3>
            {data?.encounters?.encounters?.length > 0 ? (
              <ol className="list-decimal ml-6 text-sm">
                {data.encounters.encounters.map((encounter: any, index: number) => (
                  <li key={index} className="mb-2">
                    <p>
                      <span className="font-semibold">Type:</span> {encounter.type?.[0]?.text || "Unknown"} (
                      {encounter.class || "Unknown"})
                    </p>
                    <p>
                      <span className="font-semibold">Reason:</span> {encounter.reason || "Unknown"}
                    </p>
                    <p>
                      <span className="font-semibold">Period:</span> {formatDate(encounter.period.start)} -{" "}
                      {formatDate(encounter.period.end)}
                    </p>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="text-sm">No encounters found.</p>
            )}
          </div>
        </>
      ) : (
        <p className="text-sm text-gray-500">No medical information could be found.</p>
      )}
      
    </div>
  );
};

export default PatientMedicalHistory;