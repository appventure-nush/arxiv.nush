<template>
  <v-container fluid>
    <div class="pa-4 mx-auto">
      <v-row>
        <v-col cols="12" sm="3">
          <v-list
            lines="three"
            class="text-overline bg-gray-200 fill-width fill-height py-0"
          >
            <v-list-subheader class="bg-gray-400 text-white"
              ><b>My Submissions</b></v-list-subheader
            >
            <v-list-item
              v-for="sub in allSubmissions"
              :href="`/submissions/${sub.eventId}/${sub.year}/${sub.code}`"
              :key="`${sub.eventId} ${sub.year} ${sub.code}`"
              active-color="primary"
            >
              <v-list-item-title class="text-wrap text-bold">
                <strong>{{ sub.code }}</strong>
              </v-list-item-title>
              <v-list-item-subtitle class="text-overline">
                {{ sub.eventId }} {{ sub.year }} <br />
                <!-- {{ sub.subTitle }} <br> -->
                {{ sub.projects.join(", ") }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-col>
        <v-col cols="12" sm="6">
          <div class="mx-4 pa-4">
            <div class="d-flex text-overline">
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
              <v-spacer></v-spacer>{{ submission.format ?? "" }}
              {{
                getDefn(submission.isCompetition, submission.isConference)
              }}
              Submission
            </div>

            <!-- Title Segment -->

            <h1
              v-if="!editTitle"
              @click="
                if (ownSubmission) {
                  editTitle = true;
                  tempTitle = submission.subTitle;
                }
              "
            >
              {{ submission.subTitle }}
            </h1>
            <v-text-field
              v-else
              v-model="tempTitle"
              class="mx-4"
              clearable
              v-on:keyup.enter="
                editTitle = false;
                updateTitle();
              "
              hide-details="auto"
              label="Project Title"
            ></v-text-field>

            <p class="text-overline">
              {{
                submission.start_date == submission.end_date
                  ? submission.start_date.toLocaleDateString(
                      "en-US",
                      dateOptions,
                    )
                  : `${submission.start_date.toLocaleDateString(
                      "en-US",
                      dateOptions,
                    )} - ${submission.end_date.toLocaleDateString(
                      "en-US",
                      dateOptions,
                    )}`
              }}
            </p>

            <br /><br />
            <vue-markdown
              :source="submission.subAbstract.replaceAll('\n', '<br/>')"
              :options="viewOptions"
            ></vue-markdown>
          </div>
        </v-col>

        <v-col cols="12" sm="3">
          <v-list>
            <v-list-subheader class="text-wrap"
              >Submission Members</v-list-subheader
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

              <template v-slot:append>
                <v-btn
                  v-if="submission.members.length > 1 && ownSubmission"
                  @click.stop="removeMember(member.email)"
                  size="small"
                  variant="text"
                  icon="mdi-close"
                  href=""
                ></v-btn>
              </template>
            </v-list-item>

            <v-list-item v-if="ownSubmission">
              <v-btn block color="primary" @click="submitterDialog = true"
                >ADD NEW</v-btn
              >
            </v-list-item>

            <v-list-subheader v-if="submission.accs.length > 0"
              >Accomplishments</v-list-subheader
            >
            <v-list-item
              class="text-wrap"
              v-for="acc in submission.accs"
              :key="acc.accId"
              :value="formatAward(submission, acc)"
              active-color="primary"
            >
              <v-list-item-title class="text-wrap">{{
                formatAward(submission, acc)
              }}</v-list-item-title>
            </v-list-item>

            <v-list-item v-if="ownSubmission">
              <v-btn block color="red" @click="deleteEntireSubmission()"
                >DELETE SUBMISSION</v-btn
              >
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </div>
    <NewSubmitterDialog
      v-model:visible="submitterDialog"
      :eventId="eventId"
      :year="year"
      :code="code"
    ></NewSubmitterDialog>
  </v-container>
</template>
<script lang="ts" setup>
import VueMarkdown from "vue-markdown-render";
import { ref, type Ref, computed, onMounted, watch } from "vue";
import {
  SidebarSubmission,
  StrongSubmission,
  dummySubmission,
  Award,
  Publication,
} from "@/types/project";
import {
  loadSidebarSubmissions,
  getSubmission,
  updateSubmission,
  removeStudentFromSubmission,
  deleteSubmission,
} from "@/api/projects";
import { useAppStore } from "@/store/app";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

import NewSubmitterDialog from "@/components/newAuthor/NewSubmitterDialog.vue";

import default_image from "@/assets/default.png";

const route = useRoute();
const router = useRouter();

const appStore = useAppStore();

const eventId = ref("");
const year = ref(new Date().getFullYear());
const code = ref("");

const submission = ref(dummySubmission());
const allSubmissions: Ref<SidebarSubmission[]> = ref([]);

const ownSubmission = ref(false);

const editTitle = ref(false);
const tempTitle = ref("");
const editAbstract = ref(false);
const tempAbstract = ref("");

const submitterDialog = ref(false);

function updateGeneralSubmission() {
  updateSubmission(
    eventId.value,
    year.value,
    code.value,
    submission.value.subTitle,
    submission.value.subAbstract,
  ).then((res) => (submission.value = res ?? submission.value));
}

function updateTitle() {
  submission.value.subTitle = tempTitle.value.trim() || "";
  updateGeneralSubmission();
}

function updateAbstract() {
  submission.value.subAbstract = tempAbstract.value.trim() || "";
  updateGeneralSubmission();
}

watch(submitterDialog, (dialog: boolean, prevDialog: boolean) => {
  /* ... */
  if (!dialog && prevDialog) {
    // Falling Edge lol
    getSubmission(eventId.value, year.value, code.value).then((res) => {
      submission.value = res;
      ownSubmission.value = submission.value.members
        .map((it) => it.email)
        .includes(appStore.user.email);
    });
  }
});

function removeMember(email: string) {
  removeStudentFromSubmission(
    email,
    submission.value.eventId,
    submission.value.year,
    submission.value.code,
  ).then((res) => (submission.value = res ?? submission.value));
}

async function deleteEntireSubmission() {
  if (await deleteSubmission(eventId.value, year.value, code.value))
    router.push("/submissions");
}

function getDefn(comp: boolean, conf: boolean): string {
  if (comp && conf) return "Competition & Conference";
  if (comp) return "Competition";
  if (conf) return "Conference";
  return "";
}

const viewOptions = {
  html: true, // Enable HTML tags in source
  breaks: true, // Convert '\n' in paragraphs into <br>
  linkify: true, // Autoconvert URL-like text to links
  typographer: true,
  quotes: "“”‘’",
};

const dateOptions = { year: "numeric", month: "long", day: "numeric" };

function formatAward(submission: StrongSubmission, acc: Award | Publication) {
  if ("name" in acc) {
    // Award
    if (acc.prize.length > 0) return `🏆 ${acc.name} (${acc.prize})`;
    else return `🏆 ${acc.name}`;
  } else {
    return `📰 Publication in ${submission.eventId} ${submission.year}`;
  }
}

onMounted(() => {
  eventId.value = route.params.id as string;
  year.value = parseInt(route.params.year as string);
  code.value = route.params.code as string;
  loadSidebarSubmissions(appStore.userId).then(
    (res) => (allSubmissions.value = res),
  );
  getSubmission(eventId.value, year.value, code.value).then((res) => {
    submission.value = res;
    ownSubmission.value = submission.value.members
      .map((it) => it.email)
      .includes(appStore.user.email);
  });
});
</script>
