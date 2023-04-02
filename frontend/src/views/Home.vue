<template>
  <v-container fluid class="fill-height onboarding">
    <v-responsive class="d-flex">
      <div class="text-h2 font-weight-light mb-n1">Welcome to</div>
      <h1 class="text-h1 font-weight-bold">arXiv.nush.</h1>
      <div class="py-14" />

      <div class="text-h4 mb-n1">Explore Research@NUSH like never before.</div>

      <div class="py-14" />

      <div class="align-center text-center fill-height">
        <v-row class="d-flex align-center justify-center">

        <v-col cols="auto">
          <v-btn
            color="primary"
            href="https://next.vuetifyjs.com/introduction/why-vuetify/#feature-guides"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            target="_blank"
            variant="flat"
          >
            <v-icon
              icon="mdi-speedometer"
              size="large"
              start
            />

            Enter
          </v-btn>
        </v-col>
      </v-row>

      </div>

    </v-responsive>
  </v-container>
</template>

<script lang="ts" setup>
import {
  ref,
  type Ref
} from 'vue';

</script>

<style scoped>
.onboarding {
  background: url('/src/assets/books.jpg') no-repeat center center fixed !important; background-size: cover;
  /* background-image: url('/src/assets/books.jpg'); */
  color: white;
  padding-left: 10%;
  padding-right: 10%;
}

</style>
