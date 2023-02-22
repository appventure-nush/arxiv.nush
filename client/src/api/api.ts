import {
  Project, NUSHStudent
} from "@/types/projects";

export async function getProjects(email: string): Promise<Array<Project>> {
  return await (await fetch(`/projectsByStudent?id=${email}`)).json();
}

export async function getNUSHStudentDetails(email: string): Promise<NUSHStudent> {
  return await (await fetch(`/student?id=${email}`)).json();
}
