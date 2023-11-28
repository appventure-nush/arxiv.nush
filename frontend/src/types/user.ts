import { Institute, Job } from "./admin";
export class User {
  email!: string;
  name!: string;
  pfp!: string;
}

export class Student extends User {
  nush_sid!: string;
  gradYear!: number;
  about!: string;
}

export class Coauthor extends Student {
  count!: number;
}

export class Teacher extends User {
  deptId!: string;
  isAdmin!: boolean;
  isMentor!: boolean;
}

export class ExternalTeacher {
  email!: string;
  name!: string;
  schId!: string;
}

export class ExternalStudent {
  email!: string;
  name!: string;
  emergencyEmail!: string;
  teacherName!: string;
  schId!: string;
}

export class ResearchMentor {
  email!: string;
  name!: string;
  jobs!: Job[];
}

export function dummyUser(): User {
  return { email: "", name: "", pfp: "" };
}
export function dummyStudent(): Student {
  return {
    email: "",
    name: "",
    pfp: "",
    about: "",
    nush_sid: "",
    gradYear: new Date().getFullYear(),
  };
}
export function dummyTeacher(): Teacher {
  return {
    email: "",
    name: "",
    pfp: "",
    deptId: "",
    isAdmin: false,
    isMentor: false,
  };
}

export function dummyMentor(): ResearchMentor {
  return { email: "", name: "", jobs: [] };
}
