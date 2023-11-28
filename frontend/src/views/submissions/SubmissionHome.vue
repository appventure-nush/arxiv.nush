<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <div class="mx-auto pa-4" height="100%">
          <div class="mx-4 d-flex">
            <h1>Your Submissions</h1>
            <v-spacer />
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
              v-model="submissionSearch"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </div>
          <v-row dense v-if="defaults.prefCardView">
            <v-col
              :cols="4"
              v-for="submission in searchSubmissions()"
              :key="`${submission.eventId}_${submission.year}_${submission.code}`"
              style="padding-bottom: 20px"
            >
              <v-card class="mx-auto pa-4" max-width="500px" height="100%">
                <v-flex class="text-overline">
                  <div class="mx-4 d-flex">
                    <v-breadcrumbs
                      :items="[
                        {
                          title: submission.eventId,
                          href: `/events/${submission.eventId}/${submission.year}`,
                        },
                        {
                          title: `${submission.year}`,
                          href: `/events/${submission.eventId}/${submission.year}`,
                        },
                        submission.code,
                      ]"
                      style="padding-left: 0em; padding-top: 0em"
                    ></v-breadcrumbs>
                  </div>
                </v-flex>
                <v-card-title class="text-wrap" style="word-break: normal">
                  {{ submission.subTitle }}
                </v-card-title>
                <!-- <v-card-subtitle> -->
                <!-- <p class="text-wrap mx-4" v-html="names(project)"></p> -->
                <!-- </v-card-subtitle> -->
                <v-card-actions>
                  <v-btn
                    color="primary"
                    variant="elevated"
                    :href="`/submissions/${submission.eventId}/${submission.year}/${submission.code}`"
                  >
                    Open
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          <v-data-table
            :headers="submissionHeaders"
            :items="allSubmissions"
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
            :search="submissionSearch"
            v-model:sort-by="subSortBy"
          >
            <template v-slot:item.eventId="{ item }">
              <a :href="`/events/${item.raw.eventId}/${item.raw.year}`"
                >{{ item.raw.eventId }} {{ item.raw.year }}</a
              >
            </template>
            <template v-slot:item.subTitle="{ item }">
              <a
                :href="`/submissions/${item.raw.eventId}/${item.raw.year}/${item.raw.code}`"
                >{{ item.raw.subTitle }}</a
              >
            </template>
          </v-data-table>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts" setup>
import { ref, type Ref } from "vue";
import { SidebarSubmission } from "@/types/project";
import { loadSidebarSubmissions } from "@/api/projects";
import fuzzysort from "fuzzysort";
import { useAppStore } from "@/store/app";
import { useDefaultsStore } from "@/store/defaults";

const appStore = useAppStore();
const defaults = useDefaultsStore();

const allSubmissions: Ref<SidebarSubmission[]> = ref([]);
const submissionSearch = ref("");
const subSortBy = ref([{ key: "year", order: "desc" }]);
const submissionHeaders = ref([
  { title: "Event", value: "eventId", key: "eventId", sortable: true },
  { title: "Code", value: "code", key: "code", sortable: true },
  { title: "Title", value: "subTitle", key: "subTitle", sortable: false },
  { title: "Year", value: "year", key: "year", sortable: true },
]);

if (appStore.user != null) {
  loadSidebarSubmissions(appStore.userId).then(
    (res) => (allSubmissions.value = res),
  );
}

function searchSubmissions(): SidebarSubmission[] {
  return submissionSearch.value.length == 0
    ? allSubmissions.value
    : fuzzysort
        .go(submissionSearch.value, allSubmissions.value, {
          keys: ["eventId", "year", "code", "title"],
        })
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
