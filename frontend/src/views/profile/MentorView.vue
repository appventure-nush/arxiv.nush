<template>
  <v-container fluid>
    <v-row>
      <v-col cols="3">
        <v-card class="mx-auto pa-4 text-center">
          <v-avatar size="200px" class="justify-center">
            <v-img
              :aspect-ratio="1"
              :width="250"
              :src="default_image"
              class="justify-center"
              cover
              alt="Click to select avatar"
            ></v-img>
          </v-avatar>

          <v-card-title class="justify-center text-wrap">{{
            mentor.name
          }}</v-card-title>

          <v-list class="text-left">
            <v-list-subheader v-if="mentor.jobs.length > 0"
              >Jobs</v-list-subheader
            >
            <v-list-item
              v-for="job in mentor.jobs"
              :key="job.instId"
              :value="job.role"
              active-color="primary"
            >
              <v-list-item-title
                >{{ job.role }}, {{ job.dept }}</v-list-item-title
              >
              <v-list-item-subtitle
                >{{ job.name }} ({{ job.instId }})</v-list-item-subtitle
              >
            </v-list-item>
            <v-list-subheader v-if="students.length > 0"
              >Student Collaborators</v-list-subheader
            >
            <v-list-item
              v-for="member in students"
              :key="member.email"
              :value="member.name"
              :prepend-avatar="
                'nush_sid' in member
                  ? `data:image/png;base64,${member.pfp}` ?? ''
                  : default_image
              "
              :href="`/students/${
                'nush_sid' in member ? member.nush_sid : member.email
              }`"
              active-color="primary"
            >
              <v-list-item-title class="text-wrap" style="word-break: normal">{{
                member.name
              }}</v-list-item-title>
              <v-list-item-subtitle
                class="text-wrap"
                style="word-break: normal"
                >{{
                  "nush_sid" in member ? member.nush_sid : member.email
                }}</v-list-item-subtitle
              >
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col>
        <div class="mx-auto pa-4" height="100%">
          <div class="mx-4 d-flex text-overline">
            Projects Mentored <v-spacer />
            <span
              :style="{
                color: defaults.prefCardView ? 'black' : 'primary !important',
              }"
              >Table View</span
            ><v-switch
              v-model="defaults.prefCardView"
              density="compact"
              label=""
              style="
                flex: none;
                margin-top: -5px;
                margin-right: 5px;
                margin-left: 5px;
              "
              inset
            ></v-switch
            ><span
              :style="{
                color: defaults.prefCardView ? 'primary !important' : 'black',
              }"
              >Card View</span
            >
          </div>

          <div class="pa-8">
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </div>
          <v-row dense v-if="defaults.prefCardView">
            <v-col
              :cols="6"
              v-for="project in searchProjects()"
              :key="project.pcode"
              style="padding-bottom: 20px"
            >
              <v-card class="mx-auto pa-4" max-width="500px" height="100%">
                <v-flex class="text-overline">
                  <div class="mx-4 d-flex">
                    {{ project.pcode }} <v-spacer /> {{ project.year }}
                  </div>
                </v-flex>
                <v-card-title class="text-wrap" style="word-break: normal">
                  {{ project.title }}
                </v-card-title>
                <!-- <v-card-subtitle> -->
                <p class="text-wrap mx-4" v-html="names(project)"></p>
                <!-- </v-card-subtitle> -->
                <v-card-actions>
                  <v-btn
                    color="primary"
                    variant="elevated"
                    :href="'/projects/' + project.pcode"
                  >
                    Open
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          <v-data-table
            :headers="headers"
            :items="projects"
            v-if="!defaults.prefCardView"
            item-value="name"
            multi-sort
            class="elevation-1"
            loading-text="Loading... Please wait"
            :footer-props="{
              showFirstLastPage: true,
              firstIcon: 'mdi-arrow-collapse-left',
              lastIcon: 'mdi-arrow-collapse-right',
            }"
            :search="search"
            v-model:sort-by="sortBy"
          >
            <template v-slot:item.title="{ item }">
              <a :href="`/projects/${item.raw.pcode}`">{{ item.raw.title }}</a>
            </template>
            <template v-slot:item.members="{ item }">
              <div v-html="names(item.raw)"></div>
            </template>
          </v-data-table>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts" setup>
import { FsValidationResult } from "vue-file-selector/dist";
import fuzzysort from "fuzzysort";
import { ref, computed, type Ref, onMounted } from "vue";
import {
  Student,
  dummyStudent,
  ExternalStudent,
  ResearchMentor,
  dummyMentor,
} from "@/types/user";
import { Project } from "@/types/project";
import { useRoute } from "vue-router";
import {
  loadStudent,
  loadCoauthors,
  updateStudent,
  loadMentor,
  loadMentorStudents,
} from "@/api/user";
import { loadProjects } from "@/api/projects";
import { useDefaultsStore } from "@/store/defaults";
import names from "@/util/names";
import { emit } from "process";
import { useAppStore } from "@/store/app";
import getBase64 from "@/util/getBase64";

import default_image from "@/assets/default.png";

const defaults = useDefaultsStore();
const appStore = useAppStore();

const route = useRoute();

const mid = ref("");

const mentor: Ref<ResearchMentor> = ref(dummyMentor());

const projects: Ref<Project[]> = ref([]);

const students: Ref<Array<Student | ExternalStudent>> = ref([]);

const search = ref("");

const sortBy = ref([{ key: "pcode", order: "asc" }]);

const headers = ref([
  { title: "Project Code", value: "pcode", key: "pcode", sortable: true },
  { title: "Title", value: "title", key: "title", sortable: true },
  { title: "Members", value: "members", key: "members", sortable: false },
  { title: "Year", value: "year", key: "year", sortable: true },
]);

function searchProjects(): Project[] {
  return search.value.length == 0
    ? projects.value
    : fuzzysort
        .go(
          search.value,
          projects.value.map((it) => {
            return {
              ...it,
              combinedMembers: names(it),
            };
          }),
          {
            keys: ["title", "pcode", "combinedMembers"],
          },
        )
        .filter((it) => it.score > -3000)
        .map((it) => it.obj);
}

onMounted(() => {
  mid.value = route.params.id as string;
  loadMentor(mid.value).then((res) => {
    mentor.value = res;
  });
  loadProjects(mid.value).then((res) => (projects.value = res));

  loadMentorStudents(mid.value).then((res) => (students.value = res));
});
</script>
<style>
.v-card__text,
.v-card__title {
  word-break: normal; /* maybe !important  */
}

a {
  text-decoration: none;
  color: #1867c0;
  /* font-weight: bold; */
}
</style>
