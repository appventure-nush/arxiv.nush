import { API_URL } from "./api_constants";
import { Journal } from "@/types/publication";

export async function searchJournals(): Promise<Journal[]> {
  return await(await fetch(`${API_URL}/search/journals`)).json()
}