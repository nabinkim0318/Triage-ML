interface PatientInfoProps {
  data: any;
}

const PatientMedicalHistory: React.FC<PatientInfoProps> = ({ data }) => {
  return (
    <div className="p-4 border rounded-md mt-4 overflow-auto max-h-80 w-full">
      <h2 className="text-lg font-semibold">Patient Medical History</h2>
      <pre className="text-sm mt-2 whitespace-pre-wrap break-words">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
};

export default PatientMedicalHistory;
