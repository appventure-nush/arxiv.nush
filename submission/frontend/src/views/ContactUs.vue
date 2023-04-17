<template>
<v-container fluid>
  <div class="mx-auto pa-4" height="100%">
    <h1>Contact Us</h1>


    <v-form ref="form" class="justify-center align-center text-center" lazy-validation>
      <v-row align="center" justify="center" class="ma-4">
          <v-col cols="12" sm="4">
              <h3>Email</h3>
              <v-text-field placeholder="Email" suffix="@nushigh.edu.sg" prepend-icon="mdi-card-account-details" required>
              </v-text-field>
              <v-spacer />
              <h3>Name</h3>
              <v-text-field placeholder="Your Name" prepend-icon="mdi-account" required>
              </v-text-field>
              <v-spacer />
          </v-col>
          <v-col cols="12" sm="4">
              <h3 style="margin-bottom:10px;">Query</h3>
              <v-textarea outlined size="x-large" placeholder="Your Query" required>
              </v-textarea>
              <v-spacer />
          </v-col>
      </v-row>
      <v-row align="center" justify="center" class="my-6">
          <v-btn size="x-large" color="primary" type="submit">
              Send!
          </v-btn>
      </v-row>
    </v-form>

  </div>
</v-container>
</template>
<script lang="ts" setup>

</script>
