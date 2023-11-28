import axios from "axios";

import {
  User,
  Student,
  Coauthor,
  Teacher,
  ExternalStudent,
  ResearchMentor,
} from "@/types/user";
import { API_URL } from "./api_constants";

export async function loadStudent(sid: string): Promise<Student> {
  return await (await fetch(`${API_URL}/student/${sid}`)).json();
}

export async function loadCoauthors(sid: string): Promise<Coauthor[]> {
  return await (await fetch(`${API_URL}/coauthors/${sid}`)).json();
}

export async function loadStudents(): Promise<User[]> {
  return await (await fetch(`${API_URL}/search/students`)).json();
}

export async function loadTeachers(): Promise<User[]> {
  return await (await fetch(`${API_URL}/search/teachers`)).json();
}

export async function updateStudent(
  sid: string,
  about: string,
  pfp: string,
): Promise<Student | null> {
  // update
  let student: Student | null = null;
  await axios
    .post(`${API_URL}/update/student`, { sid, about, pfp })
    .then((res) => {
      const data = res.data;
      if ("result" in data && data.result == false) return;
      student = data;
    });
  return student;
}

export async function createExternalStudent(
  email: string,
  name: string,
  teacherEmail: string,
  teacherName: string,
  instId: string,
) {
  await axios.post(`${API_URL}/addExtStudent`, {
    email,
    name,
    teacherEmail,
    teacherName,
    instId,
  });
}

export async function loadTeacher(tid: string): Promise<Teacher> {
  return await (await fetch(`${API_URL}/teacher/${tid}`)).json();
}

export async function loadTeacherStudents(
  tid: string,
): Promise<Array<Student | ExternalStudent>> {
  if (tid.includes("@")) {
    return await (await fetch(`${API_URL}/extTeacherStudents/${tid}`)).json();
  } else {
    return await (
      await fetch(`${API_URL}/bestStudents/${tid}@nushigh.edu.sg`)
    ).json();
  }
}

export async function loadMentor(mid: string): Promise<ResearchMentor> {
  return await (await fetch(`${API_URL}/mentor/${mid}`)).json();
}

export async function loadMentorStudents(
  mid: string,
): Promise<Array<Student | ExternalStudent>> {
  return await (await fetch(`${API_URL}/mentorStudents/${mid}`)).json();
}
