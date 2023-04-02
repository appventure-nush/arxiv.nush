<template>
<v-app>


  <v-navigation-drawer v-model="drawerShown" temporary app>
    <v-list dense nav>
      <v-list-item>
        <h2>Welcome, {{ firstname }} {{ lastname }}!</h2>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item v-for="item in drawerRoutes" :to="item.path" @click="drawerShown = false"
                    style="text-decoration: none; color: inherit;" :key="item.name">
        <template v-slot:prepend>
            <v-icon :icon="item.icon"></v-icon>
        </template>
        <v-list-item-title v-text="item.name"></v-list-item-title>
      </v-list-item>
    </v-list>
</v-navigation-drawer>

<v-app-bar app color="primary" dark>
    <v-app-bar-nav-icon @click="drawerShown = !drawerShown"></v-app-bar-nav-icon>
    <v-toolbar-title>
      arXiv.nush
    </v-toolbar-title>
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

import router from "./router";


/** Vuetify Theme */
const theme = useTheme();


const drawerShown: Ref<boolean> = ref(false)

const drawerRoutes = [
  {
    name: "Home",
    path: "/",
    icon: "mdi-home",
  },
  {
    name: "Dashboard",
    path: "/projects",
    icon: "mdi-file-table-box",
  },
  {
    name: "GitHub Tracker",
    path: "/github",
    icon: "mdi-github",
  },
  {
    name: "SSEF Tracker",
    path: "/ssef",
    icon: "mdi-flask",
  },
  {
    name: "Profile",
    path: "/users/h1810124",
    icon: "mdi-account"
  },
  {
    name: "Contact Us",
    path: "/contact",
    icon: "mdi-email"
  }
]


const height: ComputedRef<number> = computed(
  () => window.innerHeight
);

const width: ComputedRef<number> = computed(
  () => window.innerWidth
);
</script>
