// Utilities
import { defineStore } from "pinia";
import { User, Student, dummyStudent } from "@/types/user";
import { type Ref, computed } from "vue";
import { login, registerStudent, registerTeacher } from "@/api/auth";
import { useLocalStorage } from "@vueuse/core";
import router from "@/router";

export const useAppStore = defineStore("app", {
  state: () => {
    // const email: Ref<string> = useLocalStorage('username', '')
    // const password: Ref<string> = useLocalStorage('password', '')
    const user: Ref<User> = useLocalStorage("user", dummyStudent());
    // const user: Ref<User | null> = ref(null);
    // ref({
    //   "email": "h1810124@nushigh.edu.sg",
    //   "gradYear": 2023,
    //   "name": "Prannaya Gupta",
    //   "nush_sid": "h1810124",
    //   "pfp": ""
    // } as Student);
    // const user: ComputedRef<User | null> = computed((it) => login(email.value, password.value))
    const loggedIn = computed(() => (user.value.email ?? "").length > 0);
    const isStudent = computed(() => "nush_sid" in user.value);
    const userId = computed(() => {
      if (isStudent.value) return (user.value as Student).nush_sid as string;
      return user.value.email.split("@")[0] as string;
    });

    return {
      user,
      loggedIn,
      isStudent,
      userId,
    };
  },
  actions: {
    logout() {
      this.user = dummyStudent();
      router.push("/");
    },
    async login(username: string, password: string): Promise<string> {
      const res = await login(username, password);
      if (res) {
        this.user = res.user ?? dummyStudent();
        return res.message;
      }
      return "";
    },
    async register(
      username: string,
      password: string,
      name: string,
      isTeacher: boolean,
      formData: any,
    ): Promise<string> {
      const res = isTeacher
        ? await registerTeacher(username, password, name, formData.deptId)
        : await registerStudent(username, password, name, formData.gradYear);
      if (res) {
        this.user = res.user ?? dummyStudent();
        return res.message;
      }
      return "";
    },
  },
});
