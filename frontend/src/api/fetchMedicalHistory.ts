import { API_BASE_URL  } from "../config";

export const fetchMedicalHistory = async (data: any) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/patient/medical-history`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

    if (!response.ok) {
        throw new Error("Failed to fetch medical history");
    }

    return response.json();
};