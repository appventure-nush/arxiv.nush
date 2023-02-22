import Vue from "vue";
import VueRouter, {RouteConfig} from "vue-router";
import Main from "@/views/Home.vue";
import Dashboard from "@/views/Dashboard.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    component: Main,
  },
  {
    path: "/home",
    component: Main,
  },
  {
    path: "/dashboard",
    component: Dashboard,
  },
];

export default new VueRouter({
  routes,
});
