import axios from "axios";
import { ResearchEvent, Event, dummyEvent } from "@/types/project";

import { API_URL } from "./api_constants";

export function parseEvent(res:any): ResearchEvent {
  return {
    eventId: res.eventId,
    year: res.year,
    name: res.name,
    about: res.about,
    start_date: new Date(res.start_date),
    end_date: new Date(res.end_date),
    format: res.format,
    isCompetition: res.isCompetition,
    isConference: res.isConference,
    organisers: res.organisers,
    awardTypes: res.awardTypes ?? [],
    confDoi: res.confDoi,
    submissions: res.submissions
  }
}

export async function loadEvent(eventId: string, year: number): Promise<ResearchEvent> {
  let event: (ResearchEvent | null) = null;
  await (await fetch(`${API_URL}/event/${eventId}/${year}`)).json().then(res => {
    event = parseEvent(res)
  })
  return event ?? dummyEvent();
}

export async function loadEvents(): Promise<Event[]> {
  return await (await (await fetch(`${API_URL}/events`)).json()).map((it: any) => parseEvent(it) ?? it)
}

export async function loadOtherEvents(id: string): Promise<ResearchEvent[]> {
  return await (await fetch(`${API_URL}/otherEvents/${id}`)).json()
}

export async function createEvent(
  eventId: string, year: number, name: string, start_date: string, end_date: string,
  format: string, about: string, isCompetition: boolean, isConference: boolean, organisers: string[],
  awardTypes: string[], confDoi: string
): Promise<ResearchEvent> {
  return await axios.post(`${API_URL}/create/researchEvent`, {
    eventId, year, name, start_date, end_date, format, about, isCompetition, isConference, organisers, awardTypes, confDoi
  }).then(res => parseEvent(res.data) ?? dummyEvent)
}

export async function updateEvent(
  eventId: string, year: number, name: string, start_date: string, end_date: string,
  format: string, about: string, isCompetition: boolean, isConference: boolean, organisers: string[],
  awardTypes: string[], confDoi: string
): Promise<ResearchEvent> {
  return await axios.post(`${API_URL}/update/researchEvent`, {
    eventId, year, name, start_date, end_date, format, about, isCompetition, isConference, organisers, awardTypes, confDoi
  }).then(res => parseEvent(res.data) ?? dummyEvent)
}
