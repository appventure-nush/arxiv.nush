<template>
  <v-container fluid>
    <v-row>
      <v-col cols="3">
        <v-card class="mx-auto pa-4 text-center">
          <!-- <v-flex class="text-overline"> -->
          <div class="mx-4 d-flex text-overline">
            {{ isNush ? (student as Student).nush_sid : "External" }}
            <v-spacer />
            {{
              isNush
                ? `Y${
                    6 +
                      new Date().getFullYear() -
                      (student as Student).gradYear ?? 0
                  }`
                : (student as ExternalStudent).schId
            }}
          </div>
          <!-- </v-flex> -->
          <FileSelector
            v-if="isOwn && isNush"
            style="margin-top: 20px"
            accept-extensions=".png,.jpg,.gif"
            :multiple="false"
            :max-file-size="15 * 1024 * 1024"
            @validated="handleFilesValidated"
            @changed="handleFilesChanged"
          >
            <v-avatar v-ripple size="200px" class="justify-center">
              <v-img
                :aspect-ratio="1"
                :width="250"
                :src="`data:image/png;base64,${student.pfp}`"
                class="justify-center"
                cover
                alt="Click to select avatar"
              ></v-img>
            </v-avatar>
          </FileSelector>
          <v-avatar v-else size="200px" class="justify-center">
            <v-img
              :aspect-ratio="1"
              :width="250"
              :src="
                isNush
                  ? `data:image/png;base64,${(student as Student).pfp}`
                  : default_image
              "
              class="justify-center"
              cover
              alt="Click to select avatar"
            ></v-img>
          </v-avatar>

          <v-card-title class="justify-center text-wrap">{{
            student.name
          }}</v-card-title>

          <v-card-text
            v-if="!editAbout && isNush"
            class="justify-center"
            @click="
              if (isOwn) {
                tempAbout = student.about;
                editAbout = true;
              }
            "
          >
            {{ student.about ? student.about : "No About Inserted" }}
          </v-card-text>
          <v-text-field
            v-if="editAbout && isNush"
            clearable
            v-model="tempAbout"
            v-on:keyup.enter="
              editAbout = false;
              updateAbout();
            "
          ></v-text-field>

          <v-list class="text-left">
            <v-list-subheader>{{
              isNush ? "Common Collaborators" : "Teacher Contact"
            }}</v-list-subheader>
            <v-list-item
              v-for="member in coauthors"
              :key="member.email"
              :value="member.name"
              :prepend-avatar="
                'nush_sid' in member
                  ? `data:image/png;base64,${member.pfp}` ?? ''
                  : ''
              "
              :href="`/students/${member.nush_sid}`"
              active-color="primary"
            >
              <v-list-item-title>{{ member.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ member.nush_sid }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item
              v-if="!isNush"
              :prepend-avatar="default_image"
              :href="`/teachers/${(student as ExternalStudent).emergencyEmail}`"
            >
              <v-list-item-title>{{
                (student as ExternalStudent).teacherName
              }}</v-list-item-title>
              <v-list-item-subtitle class="text-wrap">{{
                (student as ExternalStudent).emergencyEmail
              }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col>
        <div class="mx-auto pa-4" height="100%">
          <div class="mx-4 d-flex text-overline">
            Projects Done <v-spacer />
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
import { Student, dummyStudent, ExternalStudent } from "@/types/user";
import { Project } from "@/types/project";
import { useRoute } from "vue-router";
import { loadStudent, loadCoauthors, updateStudent } from "@/api/user";
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

const sid = ref("");

const student: Ref<Student | ExternalStudent> = ref(dummyStudent());

const isNush = computed(() => "nush_sid" in student.value);

const projects: Ref<Project[]> = ref([]);

const coauthors: Ref<Student[]> = ref([]);

const isOwn = computed(() => appStore.user?.email == student.value.email);

const editAbout = ref(false);
const tempAbout = ref("");

function updateGeneralStudent() {
  updateStudent(
    student.value.nush_sid,
    student.value.about,
    student.value.pfp,
  ).then((res) => (student.value = res ?? student.value));
}

function updateAbout() {
  student.value.about = tempAbout.value;
  updateGeneralStudent();
}

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

function handleFilesValidated(result: FsValidationResult, files: File[]) {
  // console.log('Validation result: ' + result);
}

function handleFilesChanged(files: File[]) {
  const newReport = files[0];

  getBase64(newReport).then((res) => {
    student.value.pfp = res.substring(22);
    updateGeneralStudent();
  });
}

onMounted(() => {
  sid.value = route.params.id as string;
  loadStudent(sid.value).then((res) => {
    student.value = res;
  });
  loadProjects(sid.value).then((res) => (projects.value = res));

  loadCoauthors(sid.value).then((res) => (coauthors.value = res));
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
