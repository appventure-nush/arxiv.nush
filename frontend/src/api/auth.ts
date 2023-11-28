import { Student, Teacher, User } from "@/types/user";
import { AuthResult } from "@/types/api_types";
import axios from "axios";

import { API_URL } from "./api_constants";

export async function login(
  email: string,
  password: string,
): Promise<AuthResult | null> {
  let authres: AuthResult | null = null;
  await axios.post(`${API_URL}/login`, { email, password }).then((res) => {
    authres = res.data;
  });
  return authres;
}

export async function registerStudent(
  email: string,
  password: string,
  name: string,
  gradYear: number,
): Promise<AuthResult | null> {
  let authres: AuthResult | null = null;
  await axios
    .post(`${API_URL}/register`, {
      email,
      password,
      name,
      gradYear,
      isTeacher: false,
    })
    .then((res) => {
      authres = res.data;
    });
  return authres;
}

export async function registerTeacher(
  email: string,
  password: string,
  name: string,
  deptId: string,
): Promise<AuthResult | null> {
  let authres: AuthResult | null = null;
  await axios
    .post(`${API_URL}/register`, {
      email,
      password,
      name,
      deptId,
      isTeacher: true,
    })
    .then((res) => {
      authres = res.data;
    });
  return authres;
}

export async function updateDBPassword(
  email: string,
  oldPw: string,
  newPw: string,
): Promise<string> {
  return await axios
    .post(`${API_URL}/update/password`, { email, oldPw, newPw })
    .then((res) => res.data.response);
}
