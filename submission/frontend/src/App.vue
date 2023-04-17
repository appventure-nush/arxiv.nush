<template>
<v-app>


  <v-navigation-drawer v-if="appStore.loggedIn" v-model="drawerShown" temporary app>
    <v-list dense nav>
      <v-list-item style="text-decoration: none;">


        <div align="left" class="pa-2">
          <v-avatar size="80">
            <img
                :src="`data:image/png;base64,${appStore.user?.pfp}`"
              />
          </v-avatar>
        </div>
        <v-list-item-title><span style="font-weight: bold;" class="text-overline">{{ appStore.user?.name }}</span></v-list-item-title>


      </v-list-item>
      <v-divider></v-divider>
      <v-list-item v-for="item in drawerRoutes" :to="item.path" @click="drawerShown = false"
                    style="text-decoration: none; color: inherit;" :key="item.name">
        <template v-slot:prepend>
            <v-icon :icon="item.icon"></v-icon>
        </template>
        <v-list-item-title v-text="item.name"></v-list-item-title>
      </v-list-item>
      <v-divider style="border-color: black;">
      </v-divider>

      <v-list-item v-for="item in otherRoutes" :to="item.path" @click="drawerShown = false"
                    style="text-decoration: none; color: inherit;" :key="item.name">
        <template v-slot:prepend>
            <v-icon :icon="item.icon"></v-icon>
        </template>
        <v-list-item-title v-text="item.name"></v-list-item-title>
      </v-list-item>
    </v-list>
</v-navigation-drawer>

<v-app-bar app :color="'primary'" dark v-if="appStore.loggedIn">
    <v-app-bar-nav-icon @click="drawerShown = !drawerShown"></v-app-bar-nav-icon>
    <v-toolbar-title>
      arXiv.nush
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn @click="appStore.logout()" v-if="appStore.loggedIn">Logout</v-btn>
  </v-app-bar>

  <v-main>
    <router-view />
  </v-main>
</v-app>
</template>

<script lang="ts" setup>
import {
  computed,
  nextTick,
  onMounted,
  ref,
  watch,
  type ComputedRef,
  type Ref,
  type WritableComputedRef,
} from 'vue';
import { useTheme } from 'vuetify/lib/framework.mjs';


import { useAppStore } from '@/store/app'
import { Student } from './types/user';
import { loadStudent } from './api/user';


/** Vuetify Theme */
const theme = useTheme();

const appStore = useAppStore();

const drawerShown: Ref<boolean> = ref(false)


const drawerRoutes = computed(() => {
  return [
    {
      name: "Home",
      path: "/",
      icon: "mdi-home",
    },
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: "mdi-file-table-box",
    },
    {
      name: "Projects",
      path: "/projects",
      icon: "mdi-flask"
    },
    {
      name: "Submissions",
      path: "/submissions",
      icon: "mdi-trophy"
    },

  ]
})

const otherRoutes = computed(() => {
  return [
    {
      name: "Profile",
      path: `/${appStore.isStudent ? "students" : "teachers"}/${appStore.user == null ? "" : appStore.userId}`,
      icon: "mdi-account"
    },
    {
      name: "Explore",
      path: "/explore",
      icon: "mdi-magnify"
    },
    {
      name: "Events",
      path: "/events",
      icon: "mdi-calendar"
    },
    // {
    //   name: "Contact Us",
    //   path: "/contact",
    //   icon: "mdi-email"
    // },
    {
      name: "Settings",
      path: "/settings",
      icon: "mdi-cog"
    }
  ]
})



const height: ComputedRef<number> = computed(
  () => window.innerHeight
);

const width: ComputedRef<number> = computed(
  () => window.innerWidth
);

onMounted(() => {
  if('nush_sid' in (appStore.user ?? {})) {
    loadStudent((appStore.user as Student).nush_sid).then(res => appStore.user = res ?? appStore.user)
  }
})
</script>
