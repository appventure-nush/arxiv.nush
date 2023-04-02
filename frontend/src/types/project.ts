import {Student, Teacher} from "@/types/user";

export class Project {
  pcode!: string
  title!: string
  year!: number
  abstract!: string
  members!: Student[]
  teacher!: Teacher
  deptId!: string
}
