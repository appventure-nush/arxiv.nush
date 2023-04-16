<template>
<v-container fluid class="pa-4 ma-2">
  <h1 class="mx-2">Settings</h1>

  <v-col cols="12" sm="6">
    <v-btn color="primary" v-if="!changePassword" @click="changePassword = true">Change Password?</v-btn>
    <v-form :style="changePassword ? {display: 'block'} : {display: 'none'}" fast-fail @submit.prevent>
      <h3 class="mt-2">Current Password?</h3>
      <v-text-field :type="showPassword ? 'text' : 'password'" :rules="[rules.required, rules.lowerBound, rules.upperBound]"
        clearable placeholder="Current Password" v-model="oldPassword" required></v-text-field>
      <h3 class="mt-2">New Password</h3>
      <v-text-field :type="showPassword ? 'text' : 'password'" :rules="[rules.required, rules.lowerBound, rules.upperBound]"
        clearable placeholder="New Password" v-model="newPassword" required></v-text-field>
      <h3 class="mt-2">Confirm New Password</h3>
      <v-text-field :type="showPassword ? 'text' : 'password'" :rules="[rules.required, rules.lowerBound, rules.upperBound]"
        clearable placeholder="Confirm New Password" v-model="confPassword" required></v-text-field>
      <div class="d-flex mt-2">
        <v-btn color="primary" @click="showPassword = !showPassword">
          <v-icon>{{ showPassword ? 'mdi-eye' : 'mdi-eye-off' }}</v-icon>&nbsp;
          {{ showPassword ? 'Hide Passwords' : 'Show Passwords' }}
        </v-btn>
        <v-spacer></v-spacer>  <!-- This adds a gap for the buttons -->
        <v-btn color="red" @click="changePassword =!changePassword">Cancel</v-btn>
        <v-btn color="primary" type="submit" class="ml-4" :loading="passwordLoading" @click="updatePassword()">Change Password</v-btn>
      </div>
    </v-form>



  </v-col>
  <v-dialog v-model="isChangePasswordError">
    <v-card>
      <v-card-title>
        {{ changePasswordError }}
      </v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer><v-btn color="primary" @click="isChangePasswordError = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</v-container>
</template>
<script lang="ts" setup>
import {ref, type Ref, computed, onMounted} from 'vue'
import { useAppStore } from '@/store/app';
import {updateDBPassword} from '@/api/auth'

const appStore = useAppStore()


const changePassword = ref(false)

const oldPassword = ref("")
const newPassword = ref("")
const confPassword = ref("")
const showPassword = ref(false)
const passwordLoading = ref(false)
const isChangePasswordError = ref(false)
const changePasswordError = ref("")

const rules = {
  required: (v: string) => !!v || 'This field is required.', 	// if the field is empty, the error message is not shown.
  lowerBound: (v: string) => v.length >= 8 || 'Password must be at least 8 characters.',  // if the field is shorter than 8 characters, the error message
  upperBound: (v: string) => v.length <= 20 || 'Password must be at max 20 characters.',  // if the field is longer than 20 characters, the error message
}

async function updatePassword() {
  if(newPassword.value != confPassword.value) {
    changePasswordError.value = "Your passwords don't match."
    isChangePasswordError.value = true 		// if the passwords don't match, the error message is shown.
    return;
  }
  if(oldPassword.value == newPassword.value) {
    changePasswordError.value = "Your old and new passwords should not match."
    isChangePasswordError.value = true 		// if the old and new passwords match, the error message is shown.
    return;
  }

  passwordLoading.value = true;

  const response = await updateDBPassword(appStore.user.email, oldPassword.value, newPassword.value)

  passwordLoading.value = false;

  if(response != "Success!") {
    changePasswordError.value = response || "An unexpected error occured." 	// if the update password failed, the error message is shown.
    isChangePasswordError.value = true 		// if the update password failed, the error message is shown.
    return;
  }

  oldPassword.value = ""
  newPassword.value = ""
  confPassword.value = ""
  showPassword.value = false
  changePassword.value = false;

}

</script>
