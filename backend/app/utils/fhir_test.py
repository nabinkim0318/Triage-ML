import argparse
import asyncio
import json
import os
from dotenv import load_dotenv
from app.services.fhir_service import FHIRService

load_dotenv()

async def test_fhir_service(patient_id, function_name):
    """Test utility for the FHIR service"""
    fhir_server_url = os.getenv("FHIR_SERVER_URL")
    access_token = os.getenv("TEST_ACCESS_TOKEN")
    
    if not fhir_server_url:
        print("Error: FHIR_SERVER_URL not set in environment variables")
        return
        
    service = FHIRService(fhir_server_url, access_token)
    
    # Map of available function names to their corresponding methods
    functions = {
        "patient": service.get_patient,
        "demographics": service.get_patient_demographics,
        "vitals": service.get_vital_signs,
        "labs": service.get_lab_results,
        "conditions": service.get_conditions,
        "medications": service.get_medications,
        "allergies": service.get_allergies,
        "observations": service.get_observations
    }
    
    if function_name not in functions:
        print(f"Error: Unknown function '{function_name}'. Available functions: {', '.join(functions.keys())}")
        return
        
    try:
        result = await functions[function_name](patient_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error calling {function_name}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the FHIR service")
    parser.add_argument("patient_id", help="Patient ID to retrieve data for")
    parser.add_argument("function", help="Function to test", 
                        choices=["patient", "demographics", "vitals", "labs", 
                                "conditions", "medications", "allergies", "observations"])
    
    args = parser.parse_args()
    
    asyncio.run(test_fhir_service(args.patient_id, args.function))