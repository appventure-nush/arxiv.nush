import { GeneralInstitute } from "@/types/admin";

import { API_URL } from "./api_constants";

export async function searchSchools(): Promise<GeneralInstitute[]> {
  return await (await(fetch(`${API_URL}/search/schools`))).json()
}

export async function searchOrganisers(): Promise<GeneralInstitute[]> {
  return await (await(fetch(`${API_URL}/search/organisers`))).json()
}