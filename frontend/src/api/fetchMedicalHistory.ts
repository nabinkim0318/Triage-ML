import { API_BASE_URL  } from "../config";

export const fetchMedicalHistory = async (firstName:string, lastName:string, dob:string) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/patient/${firstName}/${lastName}/${dob}/medical-history`, {
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