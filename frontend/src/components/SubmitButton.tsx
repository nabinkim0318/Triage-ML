// Submit triage level

interface SubmitButtonProps {
    onSubmit: () => void;
  }
  
  const SubmitButton: React.FC<SubmitButtonProps> = ({ onSubmit }) => {
    return (
      <button
        onClick={onSubmit}
        className="mt-4 p-2 bg-green-500 text-white rounded-md w-full"
      >
        Submit Triage Decision
      </button>
    );
  };
  
  export default SubmitButton;
