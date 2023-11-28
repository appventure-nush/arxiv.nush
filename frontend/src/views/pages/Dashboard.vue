<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mx-auto pa-4" height="100%">
          <div class="mx-4 d-flex">
            <h1>Welcome, {{ appStore.user.name }}!</h1>
            <!-- <v-spacer />
          <span class="text-overline">Table View</span>
          <v-switch v-model="defaults.prefCardView"
            style="flex: none; margin-top:-5px; margin-right:5px;margin-left: 5px;"
            density='compact' label="" inset></v-switch>
          <span class="text-overline">Card View</span> -->
          </div>
        </div>
      </v-col>
    </v-row>
    <v-row style="padding-bottom: 0px">
      <v-col cols="12" md="6">
        <v-card class="pa-8" height="100%">
          <v-card-title> Upcoming Submissions </v-card-title>
          <v-timeline side="end" align="start">
            <v-timeline-item
              dot-color="teal-lighten-3"
              size="small"
              v-for="submission in submissions"
              :key="`${submission.eventId} ${submission.year} ${submission.code}`"
            >
              <div class="d-flex">
                <strong class="me-4"
                  ><span
                    v-if="
                      formatDate(submission.start_date) !=
                      formatDate(submission.start_date)
                    "
                    >{{ formatDate(submission.start_date, false) }} - </span
                  >{{ formatDate(submission.start_date) }}</strong
                >
                <div>
                  <strong
                    >{{ submission.eventId }} {{ submission.year }} -
                    {{ submission.code }}</strong
                  >
                  <div class="text-caption mb-2">
                    {{ submission.subTitle }}
                  </div>
                </div>
              </div>
            </v-timeline-item>
          </v-timeline>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card height="100%">
          <v-card-title class="pa-8">Best Projects</v-card-title>
          <v-data-table
            :headers="headers"
            :items="projectAwardStats"
            item-value="name"
            multi-sort
            loading-text="Loading... Please wait"
            :footer-props="{
              showFirstLastPage: true,
              firstIcon: 'mdi-arrow-collapse-left',
              lastIcon: 'mdi-arrow-collapse-right',
            }"
            v-model:sort-by="sortBy"
          >
            <template v-slot:item.title="{ item }">
              <a :href="`/projects/${item.raw.pcode}`">{{ item.raw.title }}</a>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="4" style="padding-bottom: 0px">
        <v-card color="green" class="mx-4" style="z-index: 10">
          <div class="justify-center align-center text-center">
            <Chart
              :size="{
                width: screenWidth > 960 ? 350 : screenWidth - 80,
                height: 250,
              }"
              :data="projStats"
              :margin="margin"
              :direction="'horizontal'"
            >
              <template #layers>
                <Grid strokeDasharray="2,2" />
                <Line
                  :dataKeys="['year', 'count']"
                  :lineStyle="{
                    stroke: '#fff',
                  }"
                />
              </template>
            </Chart>
          </div>
        </v-card>
        <v-card
          class="pa-8 mx-auto justify-center text-center fill-width"
          style="position: relative; top: -240px; margin-bottom: 0px"
          max-width="1000px"
        >
          <v-card-title style="margin-top: 220px">Your Projects</v-card-title>

          <v-card-text>
            <i>{{
              projStats
                .map((it) => it.count)
                .reduce((partialSum, a) => partialSum + a, 0) < 3
                ? "You should explore more projects!"
                : "You're excelling at research!"
            }}</i>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4" style="padding-bottom: 0px">
        <v-card color="info" class="mx-4" style="z-index: 10">
          <div class="justify-center align-center text-center">
            <Chart
              :size="{
                width: screenWidth > 960 ? 350 : screenWidth - 80,
                height: 250,
              }"
              :data="subStats"
              :margin="margin"
              :direction="'horizontal'"
            >
              <template #layers>
                <Grid strokeDasharray="2,2" />
                <Line
                  :dataKeys="['year', 'count']"
                  :lineStyle="{
                    stroke: '#fff',
                  }"
                />
              </template>
            </Chart>
          </div>
        </v-card>
        <v-card
          class="pa-8 mx-auto justify-center text-center fill-width"
          style="position: relative; top: -240px"
          max-width="1000px"
        >
          <v-card-title style="margin-top: 220px"
            >Your Submissions</v-card-title
          >

          <v-card-text>
            <i>{{
              subStats
                .map((it) => it.count)
                .reduce((partialSum, a) => partialSum + a, 0) < 3
                ? "You should explore more events!"
                : "Keep going!"
            }}</i>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="4" style="padding-bottom: 0px">
        <v-card color="error" class="mx-4" style="z-index: 10">
          <div class="justify-center align-center text-center">
            <Chart
              :size="{
                width: screenWidth > 960 ? 350 : screenWidth - 80,
                height: 250,
              }"
              :data="awardStats"
              :margin="margin"
              :direction="'horizontal'"
            >
              <template #layers>
                <Grid strokeDasharray="2,2" />
                <Line
                  :dataKeys="['year', 'count']"
                  :lineStyle="{
                    stroke: '#fff',
                  }"
                />
              </template>
            </Chart>
          </div>
        </v-card>
        <v-card
          class="pa-8 mx-auto justify-center text-center fill-width"
          style="position: relative; top: -240px"
          max-width="1000px"
        >
          <v-card-title style="margin-top: 220px">Your Awards</v-card-title>

          <v-card-text>
            <i>{{
              awardStats
                .map((it) => it.count)
                .reduce((partialSum, a) => partialSum + a, 0) < 2
                ? ""
                : "Good Job!"
            }}</i>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts" setup>
import { ref, type Ref, computed, ComputedRef } from "vue";
import { Project, SidebarSubmission, StrongSubmission } from "@/types/project";
import { loadProjects } from "@/api/projects";
import { loadSidebarSubmissions, loadStrongSubmissions } from "@/api/projects";
import { useAppStore } from "@/store/app";
import { Chart, Grid, Line } from "vue3-charts";
import { Student } from "@/types/user";
import { YearlyAggregate, ProjectAggregate, getStats } from "@/api/stats";

const appStore = useAppStore();

const projects: Ref<Project[]> = ref([]);

const allSubmissions: Ref<SidebarSubmission[]> = ref([]);

const submissions: Ref<StrongSubmission[]> = ref([]);

const margin = ref({
  left: 20,
  top: 20,
  right: 20,
  bottom: 20,
});

const projStats: Ref<YearlyAggregate[]> = ref([]);
const subStats: Ref<YearlyAggregate[]> = ref([]);
const awardStats: Ref<YearlyAggregate[]> = ref([]);
const projectAwardStats: Ref<ProjectAggregate[]> = ref([]);

const screenWidth: ComputedRef<number> = computed(() => window.innerWidth);

const headers = ref([
  { title: "Project Code", value: "pcode", key: "pcode", sortable: true },
  { title: "Title", value: "title", key: "title", sortable: true },
  { title: "Count", value: "count", key: "count", sortable: false },
  { title: "Year", value: "year", key: "year", sortable: true },
]);

const sortBy = ref([{ key: "pcode", order: "asc" }]);

function formatDate(date: Date, year: boolean = true): string {
  return date.toLocaleDateString(
    "en-US",
    year
      ? { year: "numeric", month: "short", day: "numeric" }
      : { month: "short", day: "numeric" },
  );
}

if (appStore.user != null) {
  loadProjects(appStore.userId).then((res) => (projects.value = res));

  loadSidebarSubmissions(appStore.userId).then(
    (res) => (allSubmissions.value = res),
  );

  loadStrongSubmissions(appStore.userId).then(
    (res) =>
      (submissions.value = res
        .filter((it) => it.end_date > new Date())
        .sort(
          (a: StrongSubmission, b: StrongSubmission) =>
            new Date(a.start_date) - new Date(b.start_date),
        )),
  );

  getStats(appStore.userId).then((res) => {
    projStats.value = res.projectStats;
    subStats.value = res.submissionStats;
    awardStats.value = res.awardStats;
    projectAwardStats.value = res.projectAwardStats;
    console.log(res.projectStats);
    console.log(res.submissionStats);
  });
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
