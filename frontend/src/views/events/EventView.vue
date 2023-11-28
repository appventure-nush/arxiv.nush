<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" sm="2" md="2">
        <v-list class="text-overline" v-model:opened="open">
          <v-list-subheader><b>Events</b></v-list-subheader>
          <v-list-item class="text-overline" href="/events">
            <v-list-item-title class="text-overline">Home</v-list-item-title>
          </v-list-item>
          <v-list-group
            v-for="eventId in getEventIds(events)"
            :key="eventId"
            :value="eventId"
          >
            <template v-slot:activator="{ props }">
              <v-list-item class="text-overline text-left" v-bind="props">
                <v-list-item-title class="text-overline text-center">{{
                  eventId
                }}</v-list-item-title>
              </v-list-item>
            </template>
            <v-list-item
              v-for="year in getYears(events, eventId)"
              :key="year"
              :value="eventId"
              :href="`/events/${eventId}/${year}`"
            >
              <v-breadcrumbs :items="['', `${year}`]"></v-breadcrumbs>
            </v-list-item>
          </v-list-group>
          <v-list-item
            v-if="!appStore.isStudent && (appStore.user as Teacher).isAdmin"
          >
            <v-btn color="primary" @click="newEventVisible = true" block
              >Create</v-btn
            >
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="12" sm="6" md="7">
        <div class="mx-4 pa-4">
          <div class="d-flex text-overline">
            <v-breadcrumbs
              :items="[event.eventId, `${event.year}`]"
              style="padding-left: 0em; padding-top: 0em"
            ></v-breadcrumbs>
            <v-spacer></v-spacer>{{ event.format }}
            {{ getDefn(event.isCompetition, event.isConference) }}
          </div>
          <h1>{{ event.name }} ({{ event.year }})</h1>
          <p class="text-overline">
            {{
              event.start_date == event.end_date
                ? event.start_date.toLocaleDateString("en-US", dateOptions)
                : `${event.start_date.toLocaleDateString(
                    "en-US",
                    dateOptions,
                  )} - ${event.end_date.toLocaleDateString(
                    "en-US",
                    dateOptions,
                  )}`
            }}
          </p>

          <br /><br />
          <vue-markdown
            :source="event.about.replaceAll('\n', '<br/>')"
            :options="viewOptions"
          ></vue-markdown>
          <!-- <p class="text-left">{{ event.about }}</p> -->
        </div>
      </v-col>
      <v-col cols="12" sm="4" md="3">
        <v-list class="text-left text-wrap">
          <v-list-item
            v-if="!appStore.isStudent && (appStore.user as Teacher).isAdmin"
          >
            <v-btn color="primary" @click="editEventVisible = true" block
              >Edit Page</v-btn
            >
          </v-list-item>
          <v-list-subheader
            class="text-center text-overline"
            v-if="event.organisers.length > 0"
            >Organisers</v-list-subheader
          >
          <v-list-item
            v-for="organiser in event.organisers"
            :key="organiser.instId"
            :value="organiser.name"
            active-color="primary"
          >
            <v-list-item-title class="text-wrap">{{
              organiser.name
            }}</v-list-item-title>
            <v-list-item-subtitle class="text-wrap">{{
              organiser.address
            }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-subheader
            class="text-center text-overline"
            v-if="event.awardTypes.length > 0"
            >Awards Given</v-list-subheader
          >
          <v-list-item
            v-for="award in event.awardTypes.sort(
              (a, b) => a.length - b.length,
            )"
            :key="award"
            :value="award"
            variant="tonal"
            active-color="primary"
          >
            <v-list-item-title class="text-wrap">{{ award }}</v-list-item-title>
            <!-- <v-list-item-subtitle class="text-wrap">{{ organiser.address }}</v-list-item-subtitle> -->
          </v-list-item>
          <v-list-item
            v-if="(event?.confDoi ?? '').length > 0"
            :href="`https://doi.org/${event.confDoi}`"
          >
            <v-list-item-title class="text-wrap"
              >Visit at {{ event.confDoi }}</v-list-item-title
            >
          </v-list-item>
          <v-list-item v-if="appStore.isStudent">
            <v-btn color="primary" @click="submitVisible = true" block
              >Submit my Project</v-btn
            >
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="12">
        <div class="mx-4 d-flex text-overline">Project Submissions</div>

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

          <v-row dense v-if="defaults.prefCardView">
            <v-col
              :cols="4"
              v-for="submission in searchSubmissions()"
              :key="submission.code"
              style="padding-bottom: 20px"
            >
              <v-card class="mx-auto pa-4" max-width="500px" height="100%">
                <div class="text-overline mx-4 d-flex">
                  <!-- <v-breadcrumbs :items="[event.eventId, `${event.year}`]" style="padding-left: 0em;"></v-breadcrumbs> -->
                  {{ submission.code }}
                  <v-spacer></v-spacer>{{ submission.pcode }}
                </div>
                <v-card-title class="text-wrap" style="word-break: normal">
                  {{ submission.title }}
                </v-card-title>
                <v-list>
                  <v-list-subheader class="text-wrap"
                    >Project Members</v-list-subheader
                  >
                  <v-list-item
                    v-for="member in submission.members"
                    :key="member.email"
                    :value="member.name"
                    @click="
                      router.push(
                        `/students/${
                          'nush_sid' in member ? member.nush_sid : member.email
                        }`,
                      )
                    "
                    :prepend-avatar="
                      'nush_sid' in member
                        ? `data:image/png;base64,${member.pfp}`
                        : default_image
                    "
                    active-color="primary"
                  >
                    <v-list-item-title class="text-wrap">{{
                      member.name
                    }}</v-list-item-title>
                    <v-list-item-subtitle class="text-wrap">{{
                      "nush_sid" in member ? member.nush_sid : member.email
                    }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-col>
          </v-row>

          <v-data-table
            :headers="headers"
            :items="event.submissions.filter((it) => it.pcode != '')"
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
            <template v-slot:item.code="{ item }">
              <a :href="`/submissions/${eventId}/${year}/${item.raw.code}`">{{
                item.raw.code
              }}</a>
            </template>
            <template v-slot:item.title="{ item }">
              <a :href="`/submissions/${eventId}/${year}/${item.raw.code}`">{{
                item.raw.title
              }}</a>
            </template>
            <template v-slot:item.pcode="{ item }">
              <a :href="`/projects/${item.raw.pcode}`">{{ item.raw.pcode }}</a>
            </template>
            <template v-slot:item.members="{ item }">
              <div v-html="names(item.raw.members)"></div>
            </template>
          </v-data-table>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <NewEventDialog v-model:visible="newEventVisible"></NewEventDialog>
  <EditEventDialog
    v-model:visible="editEventVisible"
    v-model:event="event"
  ></EditEventDialog>
  <SubmissionDialog
    v-model:visible="submitVisible"
    v-model:event="event"
  ></SubmissionDialog>
</template>

<script lang="ts" setup>
import fuzzysort from "fuzzysort";
import { ref, type Ref, onMounted, watch } from "vue";
import VueMarkdown from "vue-markdown-render";
import { ResearchEvent, Event, dummyEvent } from "@/types/project";
import { loadEvent, loadEvents } from "@/api/events";
import { useRoute } from "vue-router";
import NewEventDialog from "@/components/event/NewEventDialog.vue";
import EditEventDialog from "@/components/event/EditEventDialog.vue";
import SubmissionDialog from "@/components/submissions/SubmissionDialog.vue";
import { WeakSubmission } from "@/types/project";
import default_image from "@/assets/default.png";
import { useRouter } from "vue-router";
import { useDefaultsStore } from "@/store/defaults";
import { ExternalStudent, Student } from "@/types/user";
import { useAppStore } from "@/store/app";

const route = useRoute();
const router = useRouter();

const appStore = useAppStore();
const defaults = useDefaultsStore();

const eventId = ref("");
const year = ref(new Date().getFullYear());

const newEventVisible = ref(false);
const editEventVisible = ref(false);
const submitVisible = ref(false);

const headers = ref([
  {
    title: "Code",
    value: "code",
    key: "code",
    sortable: true,
    align: "center",
  },
  { title: "Title", value: "title", key: "title", sortable: true },
  {
    title: "Project Code",
    value: "pcode",
    key: "pcode",
    sortable: true,
    align: "center",
  },
  { title: "Members", value: "members", key: "members", sortable: false },
]);

function names(members: Array<Student | ExternalStudent>) {
  return members
    .map((student) => {
      if ("nush_sid" in student) {
        return `<a href="/students/${student.nush_sid}">${student.name}</a>`;
      } else return `<a href="/students/${student.email}">${student.name}</a>`;
    })
    .join(", ");
}

function searchSubmissions(): WeakSubmission[] {
  return search.value.length == 0
    ? event.value.submissions.filter((it) => it.pcode != "")
    : fuzzysort
        .go(
          search.value,
          event.value.submissions
            .filter((it) => it.pcode != "")
            .map((it: WeakSubmission) => {
              return {
                ...it,
                combinedMembers: names(it.members),
              };
            }),
          {
            keys: ["title", "pcode", "code", "combinedMembers"],
          },
        )
        .filter((it) => it.score > -3000)
        .map((it) => it.obj);
}

const search = ref("");

const sortBy = ref([{ key: "pcode", order: "asc" }]);

const viewOptions = {
  html: true, // Enable HTML tags in source
  breaks: true, // Convert '\n' in paragraphs into <br>
  linkify: true, // Autoconvert URL-like text to links
  typographer: true,
  quotes: "“”‘’",
};

const dateOptions = { year: "numeric", month: "long", day: "numeric" };

const event: Ref<ResearchEvent> = ref(dummyEvent());

const open: Ref<string[]> = ref([]);

const editAbout = ref(false);
const tempAbout = ref("");

const events: Ref<Event[]> = ref([]);

function getDefn(comp: boolean, conf: boolean): string {
  if (comp && conf) return "Competition | Conference";
  if (comp) return "Competition";
  if (conf) return "Conference";
  return "";
}

function onlyUnique(value: any, index: number, array: any[]) {
  return array.indexOf(value) === index;
}

function getEventIds(events: Event[]): string[] {
  return events.map((event) => event.eventId).filter(onlyUnique);
}

function getYears(events: Event[], eventId: string): number[] {
  return events.filter((it) => it.eventId == eventId).map((it) => it.year);
}

const updatePage = (dialog: boolean, prevDialog: boolean) => {
  if (!dialog && prevDialog) {
    loadEvent(eventId.value, year.value).then(
      (res) => (event.value = res ?? event.value),
    );
    loadEvents().then((res) => (events.value = res ?? events.value));
  }
};

watch(newEventVisible, updatePage);
watch(editEventVisible, updatePage);
watch(submitVisible, updatePage);

onMounted(() => {
  eventId.value = route.params.id as string;
  year.value = parseInt(route.params.year as string);
  loadEvent(eventId.value, year.value).then(
    (res) => (event.value = res ?? event.value),
  );
  loadEvents().then((res) => (events.value = res ?? events.value));
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
