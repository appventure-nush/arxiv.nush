<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        <v-tabs v-model="tab" direction="vertical" color="primary">
          <v-tab value="option-1">
            <v-icon start> mdi-flask </v-icon>
            Projects
          </v-tab>
          <v-tab value="option-2">
            <v-icon start> mdi-calendar-multiple </v-icon>
            Events
          </v-tab>
          <v-tab value="option-3">
            <v-icon start> mdi-book-multiple </v-icon>
            Journals
          </v-tab>
        </v-tabs>
      </v-col>
      <v-col cols="10">
        <v-window v-model="tab">
          <v-window-item value="option-1">
            <div class="mx-auto pa-4" height="100%">
              <div class="mx-4 pa-8 d-flex text-overline">
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search Projects"
                  single-line
                  hide-details
                ></v-text-field>
                <v-spacer></v-spacer>
                <v-combobox
                  label="Department"
                  :items="['BI', 'CM', 'CS', 'EL', 'HU', 'MA', 'PH', 'RE']"
                  clearable
                  variant="solo"
                  v-model="deptSearch"
                ></v-combobox>
                <v-combobox
                  label="Year"
                  :items="projects.map((it) => it.year).filter(onlyUnique)"
                  clearable
                  variant="solo"
                  v-model="yearSearch"
                ></v-combobox>
                <v-spacer />
                <span
                  :style="{
                    color: defaults.prefCardView
                      ? 'black'
                      : 'primary !important',
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
                    color: defaults.prefCardView
                      ? 'primary !important'
                      : 'black',
                  }"
                  >Card View</span
                >
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
                :items="projects.filter(filterByAdvancedSearch)"
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
                  <a :href="`/projects/${item.raw.pcode}`">{{
                    item.raw.title
                  }}</a>
                </template>
                <template v-slot:item.members="{ item }">
                  <div v-html="names(item.raw)"></div>
                </template>
              </v-data-table>
            </div>
          </v-window-item>
          <v-window-item value="option-2">
            <div class="mx-auto pa-4" height="100%">
              <div class="mx-4 pa-8 d-flex text-overline">
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search Events"
                  single-line
                  hide-details
                ></v-text-field>
                <v-spacer />
                <span
                  :style="{
                    color: defaults.prefCardView
                      ? 'black'
                      : 'primary !important',
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
                    color: defaults.prefCardView
                      ? 'primary !important'
                      : 'black',
                  }"
                  >Card View</span
                >
              </div>

              <v-row dense v-if="defaults.prefCardView">
                <v-col
                  :cols="6"
                  v-for="event in searchEvents()"
                  :key="`${event.eventId}_${event.year}`"
                  style="padding-bottom: 20px"
                >
                  <v-card class="mx-auto pa-4" max-width="500px" height="100%">
                    <div class="text-overline mx-4 d-flex">
                      <v-breadcrumbs
                        :items="[event.eventId, `${event.year}`]"
                        style="padding-left: 0em; padding-top: 0em"
                      ></v-breadcrumbs>
                      <v-spacer></v-spacer>{{ event.format }}
                      {{ getDefn(event.isCompetition, event.isConference) }}
                    </div>
                    <v-card-title class="text-wrap" style="word-break: normal">
                      {{ event.name }} ({{ event.year }})
                    </v-card-title>
                    <vue-markdown
                      class="text-wrap mx-4"
                      :source="
                        (event.about.match(
                          RegExp(/(^.*?[a-z]{2,}[.!?])\s+\W*[A-Z]/),
                        ) ?? ['', event.about])[1]
                      "
                      :options="viewOptions"
                    ></vue-markdown>
                    <v-card-actions>
                      <v-btn
                        color="primary"
                        variant="elevated"
                        :href="`/events/${event.eventId}/${event.year}`"
                      >
                        Open
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
              <v-data-table
                :headers="eventHeaders"
                :items="events"
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
                <template v-slot:item.eventId="{ item }">
                  <a :href="`/events/${item.raw.eventId}/${item.raw.year}`">{{
                    item.raw.name
                  }}</a>
                </template>
                <template v-slot:item.isCompetition="{ item }">
                  <v-checkbox-btn
                    :model-value="item.raw.isCompetition == 1 ? true : false"
                    disabled
                  ></v-checkbox-btn>
                </template>
                <template v-slot:item.isConference="{ item }">
                  <v-checkbox-btn
                    :model-value="item.raw.isConference == 1 ? true : false"
                    disabled
                  ></v-checkbox-btn>
                </template>
              </v-data-table>
            </div>
          </v-window-item>
          <v-window-item value="option-3">
            <div class="mx-auto pa-4" height="100%">
              <div class="mx-4 pa-8 d-flex text-overline">
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search Journals"
                  single-line
                  hide-details
                ></v-text-field>
                <v-spacer />
                <span
                  :style="{
                    color: defaults.prefCardView
                      ? 'black'
                      : 'primary !important',
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
                    color: defaults.prefCardView
                      ? 'primary !important'
                      : 'black',
                  }"
                  >Card View</span
                >
              </div>

              <v-row dense v-if="defaults.prefCardView">
                <v-col
                  :cols="6"
                  v-for="journal in searchAllJournals()"
                  :key="journal.issn"
                  style="padding-bottom: 20px"
                >
                  <v-card class="mx-auto pa-4" max-width="500px" height="100%">
                    <div class="text-overline mx-4 d-flex">
                      <v-spacer />{{ journal.issn }}
                    </div>
                    <v-card-title class="text-wrap" style="word-break: normal">
                      {{ journal.name }}
                    </v-card-title>
                    <v-list>
                      <v-list-subheader
                        v-if="journal.institutes.length > 0"
                        class="text-overline"
                        >Publishers</v-list-subheader
                      >
                      <v-list-item
                        v-for="institute in journal.institutes"
                        :key="institute.instId"
                        active-color="primary"
                      >
                        <v-list-item-title
                          >{{ institute.name }} ({{
                            institute.instId
                          }})</v-list-item-title
                        >
                        <v-list-item-subtitle>{{
                          institute.address
                        }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-col>
              </v-row>
              <v-data-table
                :headers="journalHeaders"
                :items="journals"
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
              </v-data-table>
            </div>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts" setup>
import fuzzysort from "fuzzysort";
import { ref, type Ref, onMounted } from "vue";
import { useDefaultsStore } from "@/store/defaults";
import { useAppStore } from "@/store/app";
import { Project, ResearchEvent } from "@/types/project";
import names from "@/util/names";
import { loadOtherProjects } from "@/api/projects";
import { loadOtherEvents } from "@/api/events";
import VueMarkdown from "vue-markdown-render";
import { Journal } from "@/types/publication";
import { searchJournals } from "@/api/journals";

const appStore = useAppStore();
const defaults = useDefaultsStore();

const projects: Ref<Project[]> = ref([]);
const events: Ref<ResearchEvent[]> = ref([]);
const journals: Ref<Journal[]> = ref([]);

function onlyUnique(value: any, index: number, array: any[]) {
  return array.indexOf(value) === index;
}

const search = ref("");

const deptSearch = ref("");
const yearSearch = ref(new Date().getFullYear());

const viewOptions = {
  html: true, // Enable HTML tags in source
  breaks: true, // Convert '\n' in paragraphs into <br>
  linkify: true, // Autoconvert URL-like text to links
  typographer: true,
  quotes: "“”‘’",
};

const sortBy = ref([{ key: "pcode", order: "asc" }]);

const headers = ref([
  { title: "Project Code", value: "pcode", key: "pcode", sortable: true },
  { title: "Title", value: "title", key: "title", sortable: true },
  { title: "Members", value: "members", key: "members", sortable: false },
  { title: "Year", value: "year", key: "year", sortable: true },
]);

const eventHeaders = ref([
  { title: "Event", value: "eventId", key: "eventId", sortable: true },
  { title: "Year", value: "year", key: "year", sortable: true },
  { title: "Format", value: "format", key: "format", sortable: true },
  {
    title: "Competition?",
    value: "isCompetition",
    key: "isCompetition",
    sortable: false,
  },
  {
    title: "Conference?",
    value: "isConference",
    key: "isConference",
    sortable: false,
  },
]);

const journalHeaders = ref([
  { title: "ISSN", value: "issn", key: "issn", sortable: true },
  { title: "Journal Name", value: "name", key: "name", sortable: true },
]);

function filterByAdvancedSearch(project: Project): boolean {
  if (deptSearch.value && yearSearch.value) {
    return (
      project.deptId == deptSearch.value && project.year == yearSearch.value
    );
  }
  if (deptSearch.value) {
    return project.deptId == deptSearch.value;
  }
  if (yearSearch.value) {
    return project.year == yearSearch.value;
  }
  return true;
}

function searchProjects(): Project[] {
  return search.value.length == 0
    ? projects.value.filter(filterByAdvancedSearch)
    : fuzzysort
        .go(
          search.value,
          projects.value.filter(filterByAdvancedSearch).map((it) => {
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
        .map((it) => it.obj)
        .slice(0, 6);
}

function searchEvents(): ResearchEvent[] {
  return search.value.length == 0
    ? events.value
    : fuzzysort
        .go(search.value, events.value, {
          keys: ["name", "eventId", "year", "about", "format"],
        })
        .filter((it) => it.score > -3000)
        .map((it) => it.obj)
        .slice(0, 6);
}

function searchAllJournals(): Journal[] {
  return search.value.length == 0
    ? journals.value
    : fuzzysort
        .go(search.value, journals.value, {
          keys: ["issn", "name"],
        })
        .filter((it) => it.score > -3000)
        .map((it) => it.obj)
        .slice(0, 6);
}

function getDefn(comp: boolean, conf: boolean): string {
  if (comp && conf) return "Competition | Conference";
  if (comp) return "Competition";
  if (conf) return "Conference";
  return "";
}

const tab = ref(0); // 0 = option-1, 1 = option-2, 2 = option-3

onMounted(() => {
  loadOtherProjects(appStore.user?.email ?? "").then(
    (res) => (projects.value = res),
  );
  loadOtherEvents(appStore.user?.email ?? "").then(
    (res) => (events.value = res),
  );
  searchJournals().then((res) => (journals.value = res));
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
