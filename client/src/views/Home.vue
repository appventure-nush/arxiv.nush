<template>
<v-container fluid
  style="background: url('img/books.jpg') no-repeat center center fixed !important; background-size: cover">
  <section align="center" justify="center" :height="height" style="fill-height:100%; margin-top:40vh;">
    <v-row align="center" justify="center">
      <v-col align="center" justify="center">
        <span style="font-size: 3em" color="white">
          arXiv.nush
        </span>
        <span style="font-size: 1.5em" class="text-wrap">
          <br />Explore Research@NUSH like never before.
        </span>
      </v-col>
    </v-row>
  </section>
  <section v-scroll-reveal.reset>
    <v-row align="center" justify="center">
      <v-col align="center" justify="center">
        <span style="font-size: 3em">
          Doing an ARP at NUS High?
        </span>
        <span style="font-size: 1.5em">
          <br />Compile all your details in one platform.
        </span>
      </v-col>
    </v-row>
  </section>
  <section v-scroll-reveal.reset>
    <v-row align="center" justify="center">
      <v-col align="center" justify="center">
        <span style="font-size: 3em">
          Enjoy more comforts!
        </span>
        <span style="font-size: 1.5em">
          <br />Submit forms, report, poster, all in one platform!
        </span>
      </v-col>
    </v-row>
  </section>
  <!-- <section v-scroll-reveal.reset>
    <v-row align="center" justify="center" style="margin-bottom: 50px">
      <v-col align="center" justify="center">
        <span style="font-size: 3em">
          Explore new projects!
        </span>
      </v-col>
    </v-row>
    <v-layout wrap justify-space-around>
      <v-flex v-for="project in projects" :key="project.id" style="flex-grow: 0; padding-bottom: 40px;">
        <v-card class="mx-auto pa-4" max-width="400px" height="100%">
          <v-flex class="text-overline">
            <div class="mx-4 d-flex">
              {{ project.code }} <v-spacer /> {{ project.year }}
            </div>
          </v-flex>
          <v-card-title class="text--primary" style="word-break: break-word; color:white;">
            {{ project.title }}
          </v-card-title>
          <v-card-subtitle>
            <component :is="names(project)" />
          </v-card-subtitle>
        </v-card>
      </v-flex>
    </v-layout>
  </section> -->
  <section v-scroll-reveal.reset>
    <v-row align="center" justify="center">
      <v-col align="center" justify="center">
        <span style="font-size: 3em">
          Ready to get started?
        </span><br><br>
        <v-btn color="primary" dark x-large href="#/dashboard">
          Let's go!
        </v-btn>
      </v-col>
    </v-row>
  </section>
</v-container>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "Home",
  data: function () {
    return {
      content: "",
      author: "",
      projects: []
    };
  },
  computed: {
    height() {
      return window.innerHeight;
    },
    width() {
      return window.innerWidth;
    },
  },
  mounted() {
    console.log(this.projects);
    window.scrollTo(0, 0);
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
  }
});

</script>
