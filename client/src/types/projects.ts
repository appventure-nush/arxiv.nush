export class Project {
  pcode!: string
  title!: string
  year!: string
  teacherEmail!: string
  studentEmail!: Array<string>
}

export class NUSHStudent {
  email!: string
  graduationYear!: number
  name!: string
  nush_sid!: string
}

export class Teacher {
  dept!: string
  email!: string
  name!: string
}
