<template>
<v-container fluid
    :style="{background: `url(${booksUrl}), no-repeat center center fixed !important`, backgroundSize: `cover`}"
  >
  <section align="center"
      justify="center" :height="height" style="fill-height:100%; margin-top:30vh;">
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        align="center"
        justify="center"
      >
        <span style="font-size: 3em" color="white">
          arXiv.nush
        </span>
        <span style="font-size: 1.5em" class="text-wrap">
          <br/>Explore Research@NUSH like never before.
        </span>
      </v-col>
    </v-row>
    <v-row align="center" justify="center" class="my-6">
        <v-btn size="x-large" color="primary" @click="appStore.loggedIn ? router.push('/dashboard') : authSection?.scrollIntoView({ behavior: 'smooth' })">
            Get Started
        </v-btn>
    </v-row>
    </section>

    <section v-scroll-reveal.reset>
      <v-row
      align="center"
      justify="center"
    >
      <v-col
        align="center"
        justify="center"
      >
        <span style="font-size: 3em">
          Doing an ARP at NUS High?
        </span>
        <span style="font-size: 1.5em">
          <br/>Compile all your details in one platform.
        </span>
      </v-col>
    </v-row>
    </section>

    <section v-scroll-reveal.reset>
      <v-row
      align="center"
      justify="center"
    >
      <v-col
        align="center"
        justify="center"
      >
        <span style="font-size: 3em">
          Enjoy more comforts!
        </span>
        <span style="font-size: 1.5em">
          <br/>Submit forms, report, poster, all in one platform!
        </span>
      </v-col>
    </v-row>
    </section>

    <section v-scroll-reveal.reset ref="authSection">
      <v-row
      align="center"
      justify="center"
    >
      <v-col
        align="center"
        justify="center" cols="10"
      >
        <span style="font-size: 3em">
          Ready to get started?
        </span><br><br>

        <div v-if="appStore.loggedIn">
          <v-btn color="primary" size="x-large" href="/projects">
            Let's go!
          </v-btn>
        </div>
        <div v-else style="background-color: #fff; color:#000;">
          <v-tabs
            v-model="tab"
            fixed-tabs
            bg-color="primary">
            <v-tab value="one">Login</v-tab>
            <v-tab value="two">Register</v-tab>
          </v-tabs>
          <v-window v-model="tab">
            <v-window-item value="one" class="mx-4">
              <v-form ref="form" fast-fail @submit.prevent>
                <v-row align="center" justify="center" class="ma-4">
                  <v-col cols="12" sm="12" md="6">
                    <h3>Email</h3>
                    <v-text-field size="x-large" v-model="email" suffix="@nushigh.edu.sg"
                      prepend-icon="mdi-email" placeholder="Your Email" required>
                    </v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <h3>Password</h3>
                    <v-text-field size="x-large"
                        v-model="password" placeholder="Password"
                        :type="showPassword ? 'text' : 'password'"
                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="showPassword = !showPassword" required>
                    </v-text-field>
                  </v-col>
                </v-row>
              </v-form>
              <v-row align="center" justify="center" class="my-6">
                  <v-btn size="x-large" color="primary" @click="signIn()">
                      Login!
                  </v-btn>
              </v-row>

            </v-window-item>
            <v-window-item value="two" class="mx-4">
              <v-form ref="form" fast-fail @submit.prevent>
                <v-row align="center" justify="center" class="ma-4">
                  <v-col cols="12" sm="12" md="6">
                    <h3>Email</h3>
                    <v-text-field size="x-large" v-model="email" suffix="@nushigh.edu.sg" :rules="[rules.required]"
                      prepend-icon="mdi-email" placeholder="Your Email" required>
                    </v-text-field>
                    <v-spacer />
                    <h3>Name</h3>
                    <v-text-field size="x-large" v-model="name" prepend-icon="mdi-card-account-details" placeholder="Your Name" :rules="[rules.required, rules.nameLowerBound, rules.nameUpperBound]" required>
                    </v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <h3>Password</h3>
                    <v-text-field size="x-large" v-model="password" placeholder="Password" :type="showPassword ? 'text' : 'password'"
                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="showPassword = !showPassword" :rules="[rules.required, passwordRules.lowerBound, passwordRules.upperBound]" required>
                    </v-text-field>
                    <h3>Confirm Password</h3>
                    <v-text-field size="x-large" v-model="confPassword" placeholder="Password" :type="showPassword ? 'text' : 'password'"
                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" :rules="[rules.required, passwordRules.lowerBound, passwordRules.upperBound, rules.confirmPassword]"
                        @click:append="showPassword = !showPassword" required>
                    </v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <h3>Are you a...</h3>
                    <br>
                    <div class="mx-4 d-flex justify-center text-center">
                    <h3>Student</h3>
          <v-switch v-model="isTeacher"
            style="flex: none; margin-top:-5px; margin-right:5px;margin-left: 5px;"
            density='compact' label="" size="x-large" inset></v-switch>
          <h3>Teacher</h3>
        </div>
                  </v-col>
                  <v-col cols="12" sm="12" md="6" v-if="isTeacher">
                    <h3>Department</h3>
                    <v-combobox
                    label="Department"
                    :items="['BI', 'CM', 'CS', 'EL', 'HU', 'MA', 'PH', 'RE']"
                    clearable
                    v-model="deptSearch"
                  ></v-combobox>
                  </v-col>
                  <v-col cols="12" sm="12" md="6" v-else>
                    <h3>Graduation Year</h3>
                    <v-text-field label="Year" v-model="gradYear"
                      :rules="[(it: string) => rules.year(parseInt(it))]" required></v-text-field>
                  </v-col>
                </v-row>
              </v-form>
              <v-row align="center" justify="center" class="my-6">
                  <v-btn size="x-large" color="primary" @click="signUp()">
                      Register
                  </v-btn>
              </v-row>
            </v-window-item>
          </v-window>
        </div>




      </v-col>
    </v-row>
    </section>

    <v-dialog
      v-model="errorDialog"
      width="auto"
    >
    <v-card>
      <v-card-title  class="pa-12">
        {{ errorText }}
      </v-card-title>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="errorDialog = false">Close</v-btn>
      </v-card-actions>

    </v-card>

    </v-dialog>
  </v-container>


</template>

<script lang="ts" setup>
import booksUrl from '@/assets/books.jpg'

import {
  ref,
  type Ref,
  computed,
  onMounted,

} from 'vue';
import { useAppStore } from '@/store/app';
import { vScrollReveal } from 'vue-scroll-reveal';
import { useRouter } from 'vue-router'
import { registerPlugins } from '@/plugins';
import { isDepsOptimizerEnabled } from 'vite';

const appStore = useAppStore()

const router = useRouter()

const tab: Ref<any> = ref(null)

const height = computed(() => window.innerHeight)
const width = computed(() => window.innerWidth)

const authSection: Ref<HTMLElement | null> = ref(null)

const email = ref("")
const password = ref("")
const confPassword = ref("")
const name = ref("")
const showPassword = ref(false)
const isTeacher = ref(false)
const deptSearch = ref("")
const gradYear = ref(new Date().getFullYear())

const errorText = ref("")
const errorDialog = ref(false)

async function signIn() {
  errorText.value = await appStore.login(`${email.value}@nushigh.edu.sg`, password.value)
  if(errorText.value.length > 0) errorDialog.value = true;
}

async function signUp() {
  if(confPassword.value != password.value) {
    errorText.value = "Your passwords don't match."
    errorDialog.value = true 		// if the passwords don't match, the error message is shown.
    return;
  }
  errorText.value = await appStore.register(`${email.value}@nushigh.edu.sg`, password.value, name.value, isTeacher.value, isTeacher.value ? { deptId: deptSearch.value } : { gradYear: gradYear.value })
  if(errorText.value.length > 0) errorDialog.value = true;

}

const rules = {
  required: (v: string) => !!v || 'This field is required.', 	// if the field is empty, the error message is not shown.
  confirmPassword(conf: string) {
    return conf == password.value || 'Passwords must match'
  },
  year(value: number | null) {
    if((value ?? 0) < 2006) return "The project should have been presented after 2005."
    if((value ?? 0) > 2099) return "The project should have been presented in the 21st Century."
  },
  nameLowerBound: (v: string) => v.length >= 3 || 'Name must be at least 3 characters.',
  nameUpperBound: (v: string) => v.length <= 100 || 'name must be at most 100 characters.',
}

const passwordRules = {
  lowerBound: (v: string) => v.length >= 8 || 'Password must be at least 8 characters.',  // if the field is shorter than 8 characters, the error message
  upperBound: (v: string) => v.length <= 20 || 'Password must be at max 20 characters.',  // if the field is longer than 20 characters, the error message
}

onMounted(() => {
})



</script>

<style scoped>

.onboarding {
  background: url(booksUrl) no-repeat center center fixed !important;
  background-size: cover;
  /* background-image: url('/src/assets/books.jpg'); */
  color: white;
  padding-left: 10%;
  padding-right: 10%;
}

img.display {
    opacity: 0;
    transition: 3s;
}

img.show {
    opacity: 1;
}

.fade-enter-active {
    transition: opacity 1s ease-in-out;
}

.fade-enter-to {
    opacity: 1;
}

.fade-enter {
    opacity: 0;
}

.v-btn:before {
    opacity: 0 !important;
}

.v-ripple__container {
    opacity: 0 !important;
}

.back-to-top {
    position: fixed;
    right: 15px;
    bottom: 15px;
    z-index: 996;
    /* background: #0078ff; */
    background: #00a8a9;
    width: 40px;
    height: 40px;
    border-radius: 50px;
    /* transition: all 0.4s; */
    align-items: center !important;
    justify-content: center !important;
    display: flex !important;
    box-sizing: border-box;
    text-decoration: none;
}

/* .flex {
    flex-grow: 0;
} */

.v-card--reveal {
    top: 0;
    opacity: 1 !important;
    position: sticky;
}

/* #app {
    background: url('../img/background.png') no-repeat center center fixed !important;
    background-size: cover;
} */

section {
    height: 100vh;
    color: white;
}

a {
    text-decoration: none;
}


</style>
