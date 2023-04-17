// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
      },
      {
        path: "/dashboard",
        name: 'Dashboard',
        component: () => import('@/views/pages/Dashboard.vue')
      },
      {
        path: "/projects",
        name: "Project Home",
        component: () => import('@/views/projects/ProjectHome.vue'),
      },
      {
        path: "/projects/:id",
        name: "Project View",
        component: () => import('@/views/projects/ProjectView.vue')
      },
      {
        path: "/students/:id",
        name: "Student Profile",
        component: () => import('@/views/profile/StudentView.vue')
      },
      {
        path: "/teachers/:id",
        name: "Teacher Profile",
        component: () => import('@/views/profile/TeacherView.vue')
      },
      {
        path: "/mentors/:id",
        name: "Mentor Profile",
        component: () => import('@/views/profile/MentorView.vue')
      },
      {
        path: "/events",
        name: "Event Home",
        component: () => import('@/views/events/EventHome.vue')
      },
      {
        path: "/events/:id/:year",
        name: "Event Profile",
        component: () => import('@/views/events/EventView.vue')
      },
      {
        path: "/submissions",
        name: "Submission Home",
        component: () => import('@/views/submissions/SubmissionHome.vue'),
      },
      {
        path: "/submissions/:id/:year/:code",
        name: "Submission Profile",
        component: () => import('@/views/submissions/SubmissionView.vue')
      },
      {
        path: "/explore",
        name: "Explore",
        component: () => import('@/views/pages/Explore.vue')
      },
      {
        path: "/settings",
        name: "Settings",
        component: () => import('@/views/pages/Settings.vue')
      },
      {
        path: "/contact",
        name: "Contact Us",
        component: () => import('@/views/ContactUs.vue')
      }
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
