<template>
  <v-container fluid>
    <v-row>
      <!-- <div class="h-screen w-screen flex items-center justify-center">
    <div class="w-10/12 h-full">
      <div class="w-full mt-5 px-2"> -->
      <v-col cols="12" md="2" class="ma-4">
        <v-list class="text-overline" v-model:opened="open">
          <v-list-subheader><b>Events</b></v-list-subheader>
          <v-list-item class="text-overline text-left" href="/events">
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
      <v-col cols="12" md="9" class="ma-4">
        <div class="ma-4">
          <h1>Event Calendar</h1>

          <p class="my-4">
            Here is a summary of the various events held over the course of the
            year. The side bar should also give you a good understanding of the
            different events. For teacher administrators, you can create events
            here too.
          </p>
        </div>
        <Calendar :events="calendarEvents">
          <template #eventDialog="props">
            <v-card
              v-if="props.eventDialogData && props.eventDialogData.title"
              class="p-4 justify-center bg-gray-100"
            >
              <div
                class="text-sm md:text-base font-bold text-gray-700 text-center"
              >
                {{ props.eventDialogData.title }}
              </div>
              <div class="mt-5">
                <div class="text-xs text-gray-700 font-medium space-y-2">
                  <h6 class="items-center space-x-2">
                    <v-icon>mdi-clock-outline</v-icon>&nbsp;&nbsp;{{
                      props.eventDialogData.time.start
                    }}
                  </h6>
                  <h6 class="items-center space-x-2 font-medium italic">
                    <v-icon>mdi-tag-outline</v-icon>&nbsp;&nbsp;{{
                      props.eventDialogData.tags
                    }}
                  </h6>
                </div>

                <vue-markdown
                  class="w-full text-xs text-gray-700 mt-5"
                  :source="props.eventDialogData.description"
                  :options="viewOptions"
                ></vue-markdown>

                <v-card-actions>
                  <v-btn
                    class="bg-gray-300 hover:bg-gray-400 text-gray-700"
                    size="small"
                    @click="props.closeEventDialog"
                  >
                    <v-icon>mdi-close</v-icon>&nbsp;Close
                  </v-btn>

                  <v-btn
                    class="bg-purple-600 hover:bg-purple-700 text-white"
                    size="small"
                    :href="props.eventDialogData.url"
                  >
                    See More
                  </v-btn>
                </v-card-actions>
              </div>
            </v-card>
          </template>
        </Calendar>
      </v-col>
      <!-- </div>

    </div>

  </div> -->
    </v-row>
    <NewEventDialog v-model:visible="newEventVisible"></NewEventDialog>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, onMounted, type Ref } from "vue";
import Calendar from "@/components/calendar/Calendar.vue";
import "@/assets/main.css";
import VueMarkdown from "vue-markdown-render";
import { ResearchEvent, Event, dummyEvent } from "@/types/project";
import { loadEvent, loadEvents } from "@/api/events";
import NewEventDialog from "@/components/event/NewEventDialog.vue";
import { useAppStore } from "@/store/app";
import { Teacher } from "@/types/user";

const appStore = useAppStore();

const events: Ref<Event[]> = ref([]);

const open: Ref<string[]> = ref([]);

const newEventVisible = ref(false);

function onlyUnique(value: any, index: number, array: any[]) {
  return array.indexOf(value) === index;
}

function getEventIds(events: Event[]): string[] {
  return events.map((event) => event.eventId).filter(onlyUnique);
}

function getYears(events: Event[], eventId: string): number[] {
  return events.filter((it) => it.eventId == eventId).map((it) => it.year);
}

const viewOptions = {
  html: true, // Enable HTML tags in source
  breaks: true, // Convert '\n' in paragraphs into <br>
  linkify: true, // Autoconvert URL-like text to links
  typographer: true,
  quotes: "“”‘’",
};

// all events data
const calendarEvents = ref([
  {
    id: 5,
    url: "/events/SSEF/2023",
    title: "SSEF 2023",
    time: {
      start: "2023-03-07 00:00",
      end: "2023-03-08 23:59",
    },
    description: "SSEF 2023 yay",
    tags: "#competition",
    competition: true,
    conference: false,
  },
  {
    id: 6,
    url: "/events/SSEF/2023",
    title: "SSEF 2023",
    time: {
      start: "2023-03-07 00:00",
      end: "2023-03-08 23:59",
    },
    description: "SSEF 2023 yay",
    tags: "#competition",
    competition: true,
    conference: false,
  },
  {
    id: 8,
    url: "/events/IRCSET/2023",
    title: "IRCSET 2023",
    time: {
      start: "2023-03-07 00:00",
      end: "2023-03-08 23:59",
    },
    description: "IRCSET 2023 yay",
    tags: "#conference",
    competition: false,
    conference: true,
  },
  {
    id: 7,
    url: "/events/SSEF/2023",
    title: "SSEF 2023",
    time: {
      start: "2023-03-07 00:00",
      end: "2023-03-08 23:59",
    },
    description: "SSEF 2023 yay",
    tags: "#competition",
    competition: true,
    conference: false,
  },
]);

onMounted(() => {
  loadEvents().then((res) => {
    events.value = res ?? events.value;

    calendarEvents.value = events.value.map((it: Event, id: number) => {
      return {
        id,
        url: `/events/${it.eventId}/${it.year}`,
        title: `${it.name} (${it.year})`,
        time: {
          start: `${it.start_date.getFullYear()}-${
            it.start_date.getMonth() < 9 ? "0" : ""
          }${it.start_date.getMonth() + 1}-${
            it.start_date.getDate() < 10 ? "0" : ""
          }${it.start_date.getDate()} 00:00`,
          end: "2023-03-08 23:59",
        },
        description: (it.about.match(
          RegExp(/(^.*?[a-z]{2,}[.!?])\s+\W*[A-Z]/),
        ) ?? ["", it.about])[1],
        tags:
          it.isCompetition && it.isConference
            ? "#competition #conference"
            : it.isCompetition
            ? "#competition"
            : it.isConference
            ? "#conference"
            : "",
        competition: it.isCompetition,
        conference: it.isConference,
      };
    });
  });
});
</script>
