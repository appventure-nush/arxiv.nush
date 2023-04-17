import {Student, Teacher, ExternalStudent, ResearchMentor, dummyTeacher} from "@/types/user";
import { Institute } from "./admin";
export class Project {
  pcode!: string
  title!: string
  year!: number
  abstract!: string
  members!: Array<Student | ExternalStudent>
  teacher!: Teacher
  deptId!: string
  reportPdf!: string
  mentors!: ResearchMentor[]
}

export class Award {
  accId!: number
  name!: string
  prize!: string
}

export class Publication {
  accId!: number
  pubTitle!: string
  doi!: string
}

export class Event {
  eventId!: string
  year!: number
  name!: string
  about!: string
  isCompetition!: boolean
  isConference!: boolean
  start_date!: Date
  end_date!: Date
}

export class WeakSubmission {
  code!: string
  title!: string
  pcode!: string
  members!: Array<Student | ExternalStudent>
}

export class ResearchEvent extends Event {
  format!: string
  organisers!: Institute[]
  awardTypes!: string[]
  confDoi!: string
  submissions!: WeakSubmission[]
}

export class Submission extends Event {
  code!: string
  members!: Array<Student | ExternalStudent>
  subTitle!: string
  subAbstract!: string
  accs!: Array<Award | Publication>
}

export class StrongSubmission extends Event {
  code!: string
  projects!: Array<Project>
  members!: Array<Student | ExternalStudent>
  subTitle!: string
  subAbstract!: string
  accs!: Array<Award | Publication>

}

export class SidebarSubmission {
  eventId!: string
  year!: number
  code!: string
  projects!: string[]
  subTitle!: string
  subAbstract!: string
}


export function dummyProject(): Project {
  return {
    pcode: "",
    title: "",
    year: (new Date()).getFullYear(),
    abstract: "",
    members: [],
    teacher: dummyTeacher(),
    deptId: "",
    reportPdf: "",
    mentors: []
  }
}

export function dummyEvent(): ResearchEvent {
  return {
    eventId: "",
    year: (new Date()).getFullYear(),
    name: "",
    start_date: new Date(),
    end_date: new Date(),
    format: "",
    isCompetition: false,
    isConference: false,
    organisers: [],
    awardTypes: [],
    confDoi: "",
    about: "",
    submissions: []
  }
}

export function dummySubmission(): StrongSubmission {
  return {
    ...(dummyEvent()),
    code: "",
    projects: [],
    members: [],
    subTitle: "",
    subAbstract: "",
    accs: []
  }
}
