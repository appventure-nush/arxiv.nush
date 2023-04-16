import {Project, Submission, StrongSubmission, SidebarSubmission} from "@/types/project";
import axios from "axios"
import { API_URL } from "./api_constants";

export async function loadProjects(id: string): Promise<Project[]> {
  return await (await fetch(`${API_URL}/projects/${id}`)).json()
}

export async function loadProject(pcode: string): Promise<Project> {
  return await (await fetch(`${API_URL}/project/${pcode}`)).json()
}

export async function loadSubmissions(pcode: string): Promise<Submission[]> {
  return await (await fetch(`${API_URL}/submissions/${pcode}`)).json()
}
export async function loadOtherProjects(id: string): Promise<Project[]> {
  return await (await fetch(`${API_URL}/otherProjects/${id}`)).json()
}

export async function updateProject(pcode: string, title: string, abstract: string, reportPdf: string): Promise<Project | null> {
  // update
  let project: Project | null = null;
  await axios.post(`${API_URL}/update/project`, { pcode, title, abstract, reportPdf }).then(res => {
    const data = res.data;
    if('result' in data && data.result == false) return;
    project = data;
  })
  return project
}

export async function removeStudent(email: string, pcode: string): Promise<Project | null> {
  // update
  let project: Project | null = null;
  await axios.post(`${API_URL}/removeStudent`, { email, pcode }).then(res => {
    const data = res.data;
    if('result' in data && data.result == false) return;
    project = data;
  })
  return project
}

export async function addStudents(students: String[], pcode: string) {
  await axios.post(`${API_URL}/addStudents`, { students, pcode })
}

export async function createProject(
  pcode: string, year: number, deptId: string,
  title: string, abstract: string, teacherEmail: string,
  authorEmails: string[]
): Promise<Project | null> {
  let project: Project | null = null;
  await axios.post(`${API_URL}/create/project`, {
    pcode, year, deptId, title, abstract, teacherEmail, authorEmails
  }).then(res => project = res.data)
  return project;
}

export async function deleteProject(
  pcode: string
): Promise<boolean> {
  return await axios.post(`${API_URL}/delete/project`, {pcode}).then(res => res.data.result)
}

export async function createSubmission(
  eventId: string, year: number, code: string,
  subTitle: string, subAbstract: string,
  pcodes: string[], authorEmails: string[]
): Promise<StrongSubmission> {
  return await axios.post(`${API_URL}/create/submission`, {eventId, year, code, subTitle, subAbstract, pcodes, authorEmails}).then(res => res.data as StrongSubmission)
}

export function parseSubmission(res:any): StrongSubmission {
  return {
    eventId: res.eventId,
    year: res.year,
    name: res.name,
    about: res.about,
    isCompetition: res.isCompetition,
    isConference: res.isConference,
    start_date: new Date(res.start_date),
    end_date: new Date(res.end_date),
    // format: res.format,
    code: res.code,
    projects: res.projects,
    members: res.members,
    subTitle: res.subTitle,
    subAbstract: res.subAbstract,
    accs: res.accs
  }
}


export async function getSubmission(eventId: string, year: number, code: string): Promise<StrongSubmission> {
  return await parseSubmission(await (await fetch(`${API_URL}/submission/${eventId}/${year}/${code}`)).json())
}


export async function updateSubmission(eventId: string, year: number, code: string, subTitle: string, subAbstract: string): Promise<StrongSubmission | null> {
  // update
  let sub: StrongSubmission | null = null;
  await axios.post(`${API_URL}/update/submission`, { eventId, year, code, subTitle, subAbstract }).then(res => {
    const data = parseSubmission(res.data);
    sub = data;
  })
  return sub
}

export async function loadSidebarSubmissions(
  id: string
): Promise<SidebarSubmission[]> {
  return (await (await fetch(`${API_URL}/submissions/user/${id}`)).json())
}

export async function loadStrongSubmissions(id: string): Promise<StrongSubmission[]> {
  return await (await (await fetch(`${API_URL}/submissions/all/${id}`)).json()).map(parseSubmission)
}

export async function removeStudentFromSubmission(email: string, eventId: string, year: number, code: string): Promise<StrongSubmission | null> {
  // update
  let  submission: StrongSubmission | null = null;
  await axios.post(`${API_URL}/submission/remove`, { email, eventId, year, code }).then(res => {
    const data = res.data;
    if('result' in data && data.result == false) return;
    submission = parseSubmission(data);
  })
  return submission
}


export async function deleteSubmission(
  eventId: string, year: number, code: string
): Promise<boolean> {
  return await axios.post(`${API_URL}/delete/submission`, {eventId, year, code}).then(res => res.data.result)
}

export async function addStudentsToSubmission(students: String[], eventId: string, year: number, code: string) {
  await axios.post(`${API_URL}/submissions/add`, { students, eventId, year, code })
}
