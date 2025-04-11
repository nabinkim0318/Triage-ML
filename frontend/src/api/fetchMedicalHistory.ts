export const fetchMedicalHistory = async (patientId: string) => {
    const response = await fetch(`http://localhost:8000/api/v1/patient/${patientId}/medical-history`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch medical history");
    }

    return response.json();
};