<template>
<v-flex>
  <v-container fluid>
    <v-card class="mx-auto pa-4" height="100%">
      <v-card-title class="text--primary">Your Projects</v-card-title>
      <!--<h1>Your Projects</h1>-->
      <v-layout wrap justify-space-around>
        <v-flex v-for="project in projects" :key="project.id" style="flex-grow: 0; padding-bottom: 40px;">
          <v-card class="mx-auto pa-4" max-width="400px" height="100%">
            <v-flex class="text-overline">
              <div class="mx-4 d-flex">
                {{ project.code }} <v-spacer /> {{ project.year }}
              </div>
            </v-flex>
            <v-card-title class="text--primary" style="word-break: break-word;">
              {{ project.title }}
            </v-card-title>
            <v-card-subtitle>
              <!--{{ project.authors }}-->
              <component :is="names(project)" />
            </v-card-subtitle>
            <v-card-actions>
              <v-btn color="primary" dark :href="'#/projects/' + project.id">
                Open
              </v-btn>
              <v-btn text v-if="!project.reveal" color="primary" @click="project.reveal = true">
                Learn More
              </v-btn>
            </v-card-actions>
            <v-expand-transition>
              <div v-if="project.reveal">
                <v-card-text class="pb-0">{{
                  project.abstract ? project.abstract : "No Abstract Inserted"
                }}</v-card-text>
                <v-card-actions class="pt-0">
                  <v-btn text color="primary" @click="project.reveal = false">
                    Close
                  </v-btn>
                </v-card-actions>
              </div>
            </v-expand-transition>
          </v-card>
        </v-flex>
      </v-layout>
    </v-card>
  </v-container>
</v-flex>
</template>
<script>
import {getProjects} from "@/api/api";


import Vue from "vue";
export default Vue.extend({
  data() {
    return {
      projects: getProjects("h1810124@nushigh.edu.sg")
    };
  },
  methods: {
    names(project) {
      return {
        template: "<p>" + project.authors.split(", ").map((name) => {
          let options = users.filter((it) => (it.name == name));
          if (options.length > 0) return `<a href="#/users/${options[0].id}">${name}</a>`;
          else return name
        }).join(", ") + "</p>"
      };
    }
  },
  mounted() {
    window.scrollTo(0, 0);
  }
});

</script>
