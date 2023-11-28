import router from "@/router/index";
import { useAppStore } from "@/store/app";

const appStore = useAppStore();
router.beforeEach(async (to, from) => {
  if (
    // make sure the user is authenticated
    !appStore.loggedIn &&
    // ❗️ Avoid an infinite redirect
    to.path !== ""
  ) {
    // redirect the user to the login page
    return "/";
  }
});
