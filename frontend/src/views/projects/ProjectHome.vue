<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mx-auto pa-4" height="100%">
          <div class="mx-4 d-flex">
            <h1>Your Projects</h1>
            <v-spacer />
            <v-btn
              color="primary"
              @click="newProjectVisible = true"
              class="mx-4 x-large"
              >Create New Project</v-btn
            >
            <span class="text-overline">Table View</span>
            <v-switch
              v-model="defaults.prefCardView"
              style="
                flex: none;
                margin-top: -5px;
                margin-right: 5px;
                margin-left: 5px;
              "
              density="compact"
              label=""
              inset
            ></v-switch>
            <span class="text-overline">Card View</span>
          </div>
          <div class="pa-8">
            <v-text-field
              v-model="projectSearch"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </div>
          <v-row dense v-if="defaults.prefCardView">
            <v-col
              :cols="4"
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
            :search="projectSearch"
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
    <NewProjectDialog v-model:visible="newProjectVisible"></NewProjectDialog>
  </v-container>
</template>
<script lang="ts" setup>
import { ref, type Ref } from "vue";
import { Project } from "@/types/project";
import { loadProjects } from "@/api/projects";
import fuzzysort from "fuzzysort";
import { useAppStore } from "@/store/app";
import { useDefaultsStore } from "@/store/defaults";
import names from "@/util/names";
import NewProjectDialog from "@/components/projects/NewProjectDialog.vue";

const appStore = useAppStore();

const defaults = useDefaultsStore();

const projects: Ref<Project[]> = ref([]);

const projectSearch = ref("");

const reveal: Ref<any> = ref({});

const newProjectVisible = ref(false);

const headers = ref([
  { title: "Project Code", value: "pcode", key: "pcode", sortable: true },
  { title: "Title", value: "title", key: "title", sortable: true },
  { title: "Members", value: "members", key: "members", sortable: false },
  { title: "Year", value: "year", key: "year", sortable: true },
]);

const sortBy = ref([{ key: "pcode", order: "asc" }]);

if (appStore.user != null) {
  loadProjects(appStore.userId).then((res) => {
    for (let i of res.map((it) => it.pcode)) {
      reveal.value[i] = false;
    }

    projects.value = res;
  });
}

function searchProjects(): Project[] {
  return projectSearch.value.length == 0
    ? projects.value
    : fuzzysort
        .go(
          projectSearch.value,
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
