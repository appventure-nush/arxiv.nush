import { Student, Teacher } from "@/types/user";

export class AuthResult {
  result!: boolean;
  message!: string;
  user!: Student | Teacher;
}
