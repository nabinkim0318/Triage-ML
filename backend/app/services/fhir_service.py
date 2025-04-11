import httpx
from fastapi import HTTPException
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class FHIRService:
    def __init__(self, base_url, access_token=None):
        self.base_url = base_url
        self.access_token = access_token
        
    def _get_headers(self):
        headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json"
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    async def _make_request(self, method, url, **kwargs):
        headers = kwargs.pop('headers', self._get_headers())
        
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Making {method} request to {url}")
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                error_detail = f"FHIR request failed: HTTP {status_code}"
                try:
                    error_body = e.response.json()
                    if "issue" in error_body:
                        error_detail += f" - {error_body['issue'][0].get('details', {}).get('text', '')}"
                except:
                    error_detail += f" - {e.response.text}"
                
                logger.error(error_detail)
                raise HTTPException(
                    status_code=status_code,
                    detail=error_detail
                )
            except httpx.RequestError as e:
                logger.error(f"FHIR request error: {str(e)}")
                raise HTTPException(
                    status_code=503, 
                    detail=f"FHIR server connection error: {str(e)}"
                )
                
    async def get_resources(self, resource_type: str, params: dict) -> dict:
        """Generic fetch for a resource type with query parameters."""
        from urllib.parse import urlencode
        query_string = urlencode(params)
        url = f"{self.base_url}/{resource_type}?{query_string}"
        return await self._make_request("GET", url)

    
    async def get_patient(self, patient_id):
        url = f"{self.base_url}/Patient/{patient_id}"
        return await self._make_request("GET", url)
    
    async def get_patient_demographics(self, patient_id):
        patient_data = await self.get_patient(patient_id)
        
        demographics = {
            "id": patient_data.get("id"),
            "name": self._extract_name(patient_data.get("name", [])),
            "gender": patient_data.get("gender"),
            "birthDate": patient_data.get("birthDate"),
            "age": self._calculate_age(patient_data.get("birthDate")),
            "address": self._extract_address(patient_data.get("address", [])),
            "phone": self._extract_telecom(patient_data.get("telecom", []), "phone"),
            "email": self._extract_telecom(patient_data.get("telecom", []), "email"),
        }
        
        return demographics
    
    async def get_observations(self, patient_id, category=None, code=None, 
                              date_from=None, date_to=None, _count=50):
        url = f"{self.base_url}/Observation?patient={patient_id}"
        
        if category:
            url += f"&category={category}"
        if code:
            url += f"&code={code}"
        if date_from:
            url += f"&date=ge{date_from}"
        if date_to:
            url += f"&date=le{date_to}"
        
        url += f"&_count={_count}&_sort=-date"
        
        return await self._make_request("GET", url)
    
    async def get_vital_signs(self, patient_id, date_from=None, date_to=None):
        observations = await self.get_observations(
            patient_id, 
            category="vital-signs",
            date_from=date_from,
            date_to=date_to
        )
        
        return self._process_observations(observations)
    
    async def get_lab_results(self, patient_id, date_from=None, date_to=None):
        observations = await self.get_observations(
            patient_id, 
            category="laboratory",
            date_from=date_from,
            date_to=date_to
        )
        
        return self._process_observations(observations)
    
    async def get_conditions(self, patient_id, clinical_status=None):
        url = f"{self.base_url}/Condition?patient={patient_id}"
        
        if clinical_status:
            url += f"&clinical-status={clinical_status}"
        
        conditions_data = await self._make_request("GET", url)
        
        processed_conditions = []
        if "entry" in conditions_data:
            for entry in conditions_data["entry"]:
                condition = entry.get("resource", {})
                
                processed_condition = {
                    "id": condition.get("id"),
                    "code": self._extract_coding(condition.get("code", {})),
                    "category": self._extract_coding(condition.get("category", [{}])[0] if condition.get("category") else {}),
                    "clinicalStatus": self._extract_coding(condition.get("clinicalStatus", {})),
                    "verificationStatus": self._extract_coding(condition.get("verificationStatus", {})),
                    "severity": self._extract_coding(condition.get("severity", {})),
                    "onsetDateTime": condition.get("onsetDateTime"),
                    "recordedDate": condition.get("recordedDate"),
                }
                processed_conditions.append(processed_condition)
        
        return {
            "conditions": processed_conditions,
            "total": len(processed_conditions)
        }
    
    async def get_medications(self, patient_id):
        url = f"{self.base_url}/MedicationRequest?patient={patient_id}&_include=MedicationRequest:medication"
        
        try:
            med_requests = await self._make_request("GET", url)
            return self._process_medications(med_requests)
        except HTTPException as e:
            if e.status_code == 404:
                url = f"{self.base_url}/MedicationStatement?patient={patient_id}&_include=MedicationStatement:medication"
                try:
                    med_statements = await self._make_request("GET", url)
                    return self._process_medications(med_statements, is_request=False)
                except HTTPException:
                    return {"medications": [], "total": 0}
            else:
                raise
    
    async def get_allergies(self, patient_id):
        url = f"{self.base_url}/AllergyIntolerance?patient={patient_id}"
        
        allergies_data = await self._make_request("GET", url)
        
        processed_allergies = []
        if "entry" in allergies_data:
            for entry in allergies_data["entry"]:
                allergy = entry.get("resource", {})
                
                processed_allergy = {
                    "id": allergy.get("id"),
                    "code": self._extract_coding(allergy.get("code", {})),
                    "type": allergy.get("type"),
                    "category": allergy.get("category", []),
                    "criticality": allergy.get("criticality"),
                    "reaction": self._extract_reactions(allergy.get("reaction", [])),
                    "recordedDate": allergy.get("recordedDate"),
                }
                processed_allergies.append(processed_allergy)
        
        return {
            "allergies": processed_allergies,
            "total": len(processed_allergies)
        }
    
    async def get_clinical_notes(self, patient_id):
        doc_references = await self.get_resources(
            resource_type="DocumentReference",
            params={
                "patient": patient_id,
                "category": "clinical-note",
                "_sort": "-date"
            }
        )
        
        diagnostic_reports = await self.get_resources(
            resource_type="DiagnosticReport",
            params={
                "patient": patient_id,
                "category": "note",
                "_sort": "-date"
            }
        )
        
        return {
            "document_references": doc_references,
            "diagnostic_reports": diagnostic_reports
        }
        
    async def get_encounters(self, patient_id):
        url = f"{self.base_url}/Encounter?patient={patient_id}&_sort=-date"
        encounters_data = await self._make_request("GET", url)

        processed_encounters = []
        if "entry" in encounters_data:
            for entry in encounters_data["entry"]:
                enc = entry.get("resource", {})
                processed_encounters.append({
                    "id": enc.get("id"),
                    "status": enc.get("status"),
                    "class": enc.get("class", {}).get("code"),
                    "type": [t.get("text") for t in enc.get("type", [])],
                    "reasonCode": [r.get("text") for r in enc.get("reasonCode", [])],
                    "period": enc.get("period", {}),
                    "serviceProvider": enc.get("serviceProvider", {}).get("display")
                })

        return {
            "encounters": processed_encounters,
            "total": len(processed_encounters)
        }
    
    def _extract_name(self, names):
        if not names:
            return ""
            
        for name in names:
            if name.get("use") == "official":
                return self._format_name(name)
        
        return self._format_name(names[0])
    
    def _format_name(self, name):
        prefix = " ".join(name.get("prefix", []))
        given = " ".join(name.get("given", []))
        family = name.get("family", "")
        suffix = " ".join(name.get("suffix", []))
        
        formatted_name = ""
        if prefix:
            formatted_name += f"{prefix} "
        if given:
            formatted_name += f"{given} "
        if family:
            formatted_name += family
        if suffix:
            formatted_name += f" {suffix}"
            
        return formatted_name.strip()
    
    def _extract_address(self, addresses):
        if not addresses:
            return {}
            
        for address in addresses:
            if address.get("use") == "home":
                return self._format_address(address)
        
        return self._format_address(addresses[0])
    
    def _format_address(self, address):
        return {
            "line": address.get("line", []),
            "city": address.get("city", ""),
            "state": address.get("state", ""),
            "postalCode": address.get("postalCode", ""),
            "country": address.get("country", "")
        }
    
    def _extract_telecom(self, telecoms, system_type):
        for telecom in telecoms:
            if telecom.get("system") == system_type:
                return telecom.get("value", "")
        return ""
    
    def _calculate_age(self, birth_date):
        if not birth_date:
            return None
            
        import datetime
        from dateutil import relativedelta
        
        try:
            dob = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
            today = datetime.date.today()
            age = relativedelta.relativedelta(today, dob)
            return age.years
        except ValueError:
            return None
    
    def _extract_coding(self, coded_concept):
        result = {
            "text": coded_concept.get("text", "")
        }
        
        if "coding" in coded_concept:
            for coding in coded_concept["coding"]:
                result["code"] = coding.get("code", "")
                result["display"] = coding.get("display", "")
                result["system"] = coding.get("system", "")
                break
                
        return result
    
    def _process_observations(self, observations_data):
        processed_observations = []
        
        if "entry" in observations_data:
            for entry in observations_data["entry"]:
                obs = entry.get("resource", {})
                
                processed_obs = {
                    "id": obs.get("id"),
                    "code": self._extract_coding(obs.get("code", {})),
                    "effectiveDateTime": obs.get("effectiveDateTime"),
                    "issued": obs.get("issued"),
                    "status": obs.get("status"),
                    "category": [self._extract_coding(cat) for cat in obs.get("category", [])],
                }
                
                if "valueQuantity" in obs:
                    value = obs["valueQuantity"]
                    processed_obs["value"] = {
                        "value": value.get("value"),
                        "unit": value.get("unit"),
                        "system": value.get("system"),
                        "code": value.get("code")
                    }
                elif "valueString" in obs:
                    processed_obs["value"] = {"value": obs["valueString"]}
                elif "valueBoolean" in obs:
                    processed_obs["value"] = {"value": obs["valueBoolean"]}
                elif "valueInteger" in obs:
                    processed_obs["value"] = {"value": obs["valueInteger"]}
                elif "valueCodeableConcept" in obs:
                    processed_obs["value"] = {"value": self._extract_coding(obs["valueCodeableConcept"])}
                elif "component" in obs:
                    components = []
                    for component in obs["component"]:
                        comp_data = {
                            "code": self._extract_coding(component.get("code", {})),
                        }
                        
                        if "valueQuantity" in component:
                            value = component["valueQuantity"]
                            comp_data["value"] = {
                                "value": value.get("value"),
                                "unit": value.get("unit"),
                                "system": value.get("system"),
                                "code": value.get("code")
                            }
                        elif "valueString" in component:
                            comp_data["value"] = {"value": component["valueString"]}
                        elif "valueBoolean" in component:
                            comp_data["value"] = {"value": component["valueBoolean"]}
                        elif "valueInteger" in component:
                            comp_data["value"] = {"value": component["valueInteger"]}
                        elif "valueCodeableConcept" in component:
                            comp_data["value"] = {"value": self._extract_coding(component["valueCodeableConcept"])}
                            
                        components.append(comp_data)
                    
                    processed_obs["components"] = components
                
                processed_observations.append(processed_obs)
        
        return {
            "observations": processed_observations,
            "total": len(processed_observations)
        }
    
    def _process_medications(self, medications_data, is_request=True):
        processed_medications = []
        resource_type = "MedicationRequest" if is_request else "MedicationStatement"
        
        if "entry" in medications_data:
            medications = {}
            for entry in medications_data["entry"]:
                resource = entry.get("resource", {})
                if resource.get("resourceType") == "Medication":
                    med_id = resource.get("id", "")
                    medications[med_id] = resource
            
            for entry in medications_data["entry"]:
                resource = entry.get("resource", {})
                if resource.get("resourceType") == resource_type:
                    med_request = resource
                    
                    medication_info = {}
                    if "medicationReference" in med_request:
                        med_ref = med_request["medicationReference"].get("reference", "")
                        med_id = med_ref.replace("Medication/", "")
                        medication = medications.get(med_id, {})
                        medication_info = self._extract_medication_info(medication)
                    elif "medicationCodeableConcept" in med_request:
                        medication_info = self._extract_coding(med_request["medicationCodeableConcept"])
                    
                    dosage_info = []
                    if "dosageInstruction" in med_request:
                        for dosage in med_request["dosageInstruction"]:
                            dosage_data = {
                                "text": dosage.get("text", ""),
                                "timing": self._extract_timing(dosage.get("timing", {})),
                                "route": self._extract_coding(dosage.get("route", {})),
                                "method": self._extract_coding(dosage.get("method", {})),
                            }
                            
                            if "doseAndRate" in dosage:
                                dose_rate = dosage["doseAndRate"][0] if dosage["doseAndRate"] else {}
                                if "doseQuantity" in dose_rate:
                                    dose_data = dose_rate["doseQuantity"]
                                    dosage_data["dose"] = {
                                        "value": dose_data.get("value"),
                                        "unit": dose_data.get("unit")
                                    }
                                    
                            dosage_info.append(dosage_data)
                    
                    processed_med = {
                        "id": med_request.get("id"),
                        "status": med_request.get("status"),
                        "medication": medication_info,
                        "dosage": dosage_info,
                        "authoredOn": med_request.get("authoredOn"),
                    }
                    
                    if is_request:
                        processed_med["intent"] = med_request.get("intent")
                        if "requester" in med_request:
                            processed_med["requester"] = med_request["requester"].get("display", "")
                            
                    processed_medications.append(processed_med)
        
        return {
            "medications": processed_medications,
            "total": len(processed_medications)
        }
    
    def _extract_medication_info(self, medication):
        result = {
            "text": medication.get("text", "")
        }
        
        if "code" in medication:
            result.update(self._extract_coding(medication["code"]))
            
        return result
    
    def _extract_timing(self, timing):
        result = {}
        
        if "code" in timing:
            result["code"] = self._extract_coding(timing["code"])
            
        if "repeat" in timing:
            repeat = timing["repeat"]
            result["frequency"] = repeat.get("frequency")
            result["period"] = repeat.get("period")
            result["periodUnit"] = repeat.get("periodUnit")
            
        return result
    
    def _extract_reactions(self, reactions):
        processed_reactions = []
        
        for reaction in reactions:
            reaction_data = {
                "manifestation": [self._extract_coding(m) for m in reaction.get("manifestation", [])],
                "severity": reaction.get("severity")
            }
            processed_reactions.append(reaction_data)
            
        return processed_reactions