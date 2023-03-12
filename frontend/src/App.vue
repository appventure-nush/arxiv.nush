<template>
<v-app>
  <!-- Navigation Drawer! -->
  <v-navigation-drawer v-if="loggedIn" v-model="drawerShown" temporary app>
    <v-list dense nav>
      <v-list-item>
        <v-icon size="100">mdi-account</v-icon>
        <h2>
          Welcome, {{username}}!
        </h2>
      </v-list-item>
      <v-divider></v-divider>
      <router-link v-for="item in drawerRoutes" :to="item.path" @click="drawerShown = false"
        style="text-decoration: none; color: inherit;" :key="item.name">
        <v-list-item link :title="item.name" :prepend-icon="item.icon">
        </v-list-item>
        <v-divider />
      </router-link>
      <v-list-item
      @click="logout()"
      prepend-icon="mdi-account-cancel"
      title="Logout"
      color="primary">
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-app-bar v-if="loggedIn" app color="primary" dark>
    <v-app-bar-nav-icon v-if="loggedIn" @click="drawerShown = !drawerShown"></v-app-bar-nav-icon>
    <v-toolbar-title>
      arXiv.nush
    </v-toolbar-title>
  </v-app-bar>

  <v-app-bar v-else app dense fixed dark shrink-on-scroll prominent fade-img-on-scroll :height="height" src="@/assets/books.jpg"
    alt class="icon" key="@/assets/books.jpg" :class="imgIsLoaded ? 'show,display' : 'display'" loading="lazy" @load="imgLoaded">
    <v-container fill-width :fill-height="!hideSubtitle" fluid>
      <v-row align="center" justify="center">
        <v-col :align="(hideSubtitle) ? 'left' : 'center'" justify="center">
          <v-toolbar-title class="text-wrap" :style="{ padding: 0, color: 'white', 'font-weight': 500 }">
            <span :style="{ 'font-size': Math.max((width < 333 ? 0.75 : 1) * font, 1) + 'em' }">arXiv.nush</span>
            <span v-if="!hideSubtitle" class="text-wrap" :style="{ 'font-size': Math.min(1, font) + 'em' }">
              <br>
              Explore Research@NUSH like never before.
            </span>
          </v-toolbar-title>
          <!-- <a v-if="!hideSubtitle" href="#" v-scroll-to="'#intro'" class="back-to-top">
            <v-icon>mdi-arrow-down</v-icon>
          </a> -->
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>


  <!-- <v-app-bar app color="primary" dark>
                <v-app-bar-nav-icon v-if="loggedIn" @click="drawerShown = !drawerShown"></v-app-bar-nav-icon>
                <v-toolbar-title>
                    The Interface
                </v-toolbar-title>
            </v-app-bar> -->

  <v-main v-if="loggedIn">
    <router-view />
  </v-main>
  <v-main v-else :style="{ 'margin-top': height + 'px', minHeight: height + 'px' }">
    <v-container fluid fill-height fill-width align="center" justify="center" id="intro">
      <v-row align="center" justify="center">
        <v-col align="center" justify="center" cols="24" sm="8">
          <span>
            <span style="font-size: 2em">
              Welcome to arXiv.nush!
            </span><br>
            This platform aims to help students consolidate their research
            projects on a proper platform. <br><br>
            Perform Research, the real way!
          </span>
          <v-tabs grow center-active v-model="tab" background-color="transparent">
            <v-tab v-for="item in loginItems" :key="item">
              {{ item }}
            </v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item :key="'Login'">
              <v-form ref="form" lazy-validation>
                <v-row align="center" justify="center" class="ma-4">
                  <v-col cols="12" sm="4">
                    <h3>Username</h3>
                    <v-text-field x-large v-model="username" placeholder="Your Username" hint="root" required>
                    </v-text-field>
                    <v-spacer />
                  </v-col>
                  <v-col cols="12" sm="4">
                    <h3>Password</h3>
                    <v-text-field x-large v-model="password" placeholder="Password"
                      :type="showPassword ? 'text' : 'password'" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                      hint="admin" @click:append="showPassword = !showPassword" required>
                    </v-text-field>
                  </v-col>
                </v-row>
              </v-form>
              <v-row align="center" justify="center" class="my-6">
                <v-btn x-large color="primary" @click="login()">
                  Login!
                </v-btn>
              </v-row>
            </v-tab-item>
            <v-tab-item :key="'Register'">
              <v-form ref="form" lazy-validation>
                <v-row align="center" justify="center" class="ma-4">
                  <v-col cols="12" sm="4">
                    <h3>Username</h3>
                    <v-text-field x-large v-model="username" placeholder="Your Username" hint="root" required>
                    </v-text-field>
                    <v-spacer />
                  </v-col>
                  <v-col cols="12" sm="4">
                    <h3>Password</h3>
                    <v-text-field x-large v-model="password" placeholder="Password"
                      :type="showPassword ? 'text' : 'password'" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                      hint="admin" @click:append="showPassword = !showPassword" required>
                    </v-text-field>
                  </v-col>
                </v-row>
              </v-form>
              <v-row align="center" justify="center" class="my-6">
                <v-btn x-large color="primary" @click="register()">
                  Register!
                </v-btn>
              </v-row>
            </v-tab-item>
          </v-tabs-items>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <v-footer :padless="true">
    <v-card dark flat tile width="100%" class="text-center lighten-1">
      <v-card-text>
        An app for those who care to question.
      </v-card-text>
      <v-divider></v-divider>
      <v-card-text class="white--text">
        Developed by Prannaya Gupta
      </v-card-text>
    </v-card>
  </v-footer>
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

import books from "@/assets/books.jpg";

console.log(books);


/** Vuetify Theme */
const theme = useTheme();

/** drawer visibility */
const drawerShown: Ref<boolean> = ref(false);

/** drawer visibility */
const loggedIn: Ref<boolean> = ref(true);

const username: Ref<string> = ref("");
const password: Ref<string> = ref("");

const showPassword: Ref<boolean> = ref(false);


const font: Ref<number> = ref(window.innerWidth < 1000 ? 3 * 0.75 : 3);
const hideSubtitle: Ref<boolean> = ref(false);

const img: Ref<string> = ref(books);
const imgIsLoaded: Ref<boolean> = ref(false);

const tab: Ref<string | null> = ref(null);

const loginItems = ["Login", "Register"];


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

function login() {
  console.log(`Username: ${username.value}`);
  console.log(`Password: ${password.value}`);
  if (username.value == "root" && password.value == "admin") {
    console.log("Logged In Successfully!");
    loggedIn.value = true;
  }
  router.push("/");
}
function register() {
  console.log(`Username: ${username.value}`);
  console.log(`Password: ${password.value}`);
  console.log("Registered Successfully!");
  loggedIn.value = true;
  router.push("/");
}
function logout() {
  username.value = "";
  password.value = "";
  loggedIn.value = false;
  router.push("/");
  drawerShown.value = false;
}

function imgLoaded() {
  imgIsLoaded.value = true;
}

const height: ComputedRef<number> = computed(
  () => window.innerHeight
);

const width: ComputedRef<number> = computed(
  () => window.innerWidth
);
</script>
