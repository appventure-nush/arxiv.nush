export class User {
  email!: string
  name!: string
  pfp!: string
}

export class Student extends User {
  nush_sid!: string
  gradYear!: number
}

export class Teacher extends User {
  deptId!: string
  isAdmin!: boolean
  isMentor!: boolean
}
