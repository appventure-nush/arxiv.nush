<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" class="mx-auto">
        <!-- <v-card class="mx-auto pa-4" height="100%"> -->
        <!-- <v-flex class="text-overline"> -->
        <div class="mx-4 d-flex text-overline">
          {{ project.pcode }} <v-spacer /> {{ project.year }}
        </div>
        <!-- </v-flex> -->
        <h1
          v-if="!editTitle"
          class="mx-4 ptitle"
          @click="
            if (ownProject) {
              editTitle = true;
              tempTitle = project.title;
            }
          "
        >
          {{ project.title }}
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
        <!-- <v-card-subtitle> -->
        <!--{{ project.authors }}-->
        <div v-html="names(project)" class="mx-4" />
        <!-- </v-card-subtitle> -->
        <!-- <v-spacer /> -->
        <!-- <MdEditor v-model="tempAbstract" language="en-US" /> -->
        <!-- <mavon-editor v-model="tempAbstract"/> -->
        <!-- </v-card> -->
      </v-col>
      <v-col cols="12" md="8" min-width="400px">
        <v-card class="mx-auto pa-4">
          <!-- height="100%" -->
          <!-- <v-card-title style="text-h2">Project Abstract</v-card-title> -->
          <div class="mx-4 d-flex text-overline">Project Abstract</div>
          <div v-if="!editAbstract">
            <v-card-text>
              {{ project.abstract ? project.abstract : "No Abstract Inserted" }}
            </v-card-text>
            <v-row class="mx-4" v-if="ownProject">
              <v-col cols="12" sm="12" md="6">
                <label id="counter"
                  >({{ wordCount(project.abstract) }} words)</label
                >
              </v-col>
              <v-col cols="3" sm="12" md="6" class="text-right">
                <v-btn
                  icon="mdi-pencil"
                  style="justify: right"
                  color="primary"
                  @click="
                    editAbstract = true;
                    tempAbstract = project.abstract;
                  "
                >
                </v-btn>
              </v-col>
            </v-row>
          </div>
          <div class="mx-4" v-if="editAbstract">
            <v-textarea
              clearable
              auto-grow
              v-model="tempAbstract"
              clear-icon="mdi-close-circle"
              label="Text"
            ></v-textarea>
            <v-row>
              <v-col cols="12" sm="12" md="6">
                <label id="counter"
                  >({{ wordCount(tempAbstract) }} words)</label
                >
              </v-col>
              <v-col cols="3" sm="12" md="6" class="text-right">
                <v-btn
                  icon="mdi-content-save"
                  color="primary"
                  @click="
                    editAbstract = false;
                    updateAbstract();
                  "
                >
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" class="mx-auto pa-4" height="100%">
        <div class="mx-4 d-flex text-overline">Project Admin</div>
        <v-list>
          <v-list-subheader class="text-wrap">Project Members</v-list-subheader>
          <v-list-item
            v-for="member in project.members"
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
                v-if="project.members.length > 1 && ownProject"
                @click.stop="removeMember(member.email)"
                size="small"
                variant="text"
                icon="mdi-close"
                href=""
              ></v-btn>
            </template>
          </v-list-item>

          <v-list-item v-if="ownProject">
            <v-btn block color="primary" @click="newAuthorDialogVisible = true"
              >ADD NEW</v-btn
            >
          </v-list-item>

          <v-list-subheader
            v-if="
              project.mentors != null &&
              project.mentors != undefined &&
              project.mentors.length > 0
            "
            >Research Mentor(s)</v-list-subheader
          >
          <v-list-item
            v-for="mentor in project.mentors"
            :key="mentor.email"
            :value="mentor.name"
            active-color="primary"
            :prepend-avatar="default_image"
            :href="`/mentors/${mentor.email}`"
          >
            <v-list-item-title>{{ mentor.name }}</v-list-item-title>
            <v-list-item-subtitle>{{
              mentor.jobs.length > 0
                ? `${mentor.jobs[0].role}, ${mentor.jobs[0].instId}`
                : mentor.email
            }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-subheader v-if="project.teacher != null"
            >Teacher Mentor</v-list-subheader
          >
          <v-list-item
            :prepend-avatar="
              `data:image/png;base64,${project.teacher.pfp}` ?? ''
            "
            :href="`/teachers/${project.teacher.email.split('@')[0]}`"
            v-if="project.teacher != null"
          >
            <v-list-item-title>{{ project.teacher.name }}</v-list-item-title>
            <v-list-item-subtitle>{{
              project.teacher.email
            }}</v-list-item-subtitle>
          </v-list-item>

          <v-list-item v-if="ownProject">
            <v-btn block color="red" @click="deleteEntireProject()"
              >DELETE PROJECT</v-btn
            >
          </v-list-item>
        </v-list>
      </v-col>

      <v-col cols="12" style="margin-bottom: 20px">
        <div class="mx-4 d-flex text-overline" style="margin-top: 20px">
          Project Report
        </div>
        <v-card
          :style="
            ownProject ? { 'background-color': '#aaa' } : { height: '80vh' }
          "
          class="text-center justify-center"
          height="100%"
        >
          <PDFViewer
            :source="`data:application/pdf;base64,${project.reportPdf}`"
            :style="{ height: ownProject ? '80vh' : '100%', width: '100%' }"
          /><!-- @download="handleDownload"   v-if="ownProject" -->
          <FileSelector
            v-if="ownProject"
            style="margin-top: 20px"
            accept-extensions=".pdf"
            :multiple="false"
            :max-file-size="15 * 1024 * 1024"
            @validated="handleFilesValidated"
            @changed="handleFilesChanged"
          >
            <v-btn block color="primary">
              Click here to upload a new Report
            </v-btn>
          </FileSelector>
        </v-card>
      </v-col>

      <v-col
        cols="6"
        style="margin-top: 20px"
        class="mx-auto pa-4"
        height="100%"
        v-if="submissions.length > 0"
      >
        <div class="mx-4 d-flex text-overline">Project Submissions</div>
        <v-expansion-panels style="margin-top: 20px">
          <v-expansion-panel
            v-for="submission in submissions"
            :key="`${submission.eventId}_${submission.year}_${submission.code}`"
          >
            <v-expansion-panel-title>
              <template v-slot:default="{ expanded }">
                <span v-if="!expanded"
                  ><b
                    >{{ submission.eventId }} {{ submission.year }}:
                    {{ submission.code }}</b
                  ></span
                >
                <span v-else>{{ submission.subTitle }}</span>
              </template>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <p style="subtitle-2">
                {{ submission.subAbstract }}
              </p>

              <v-list v-if="submission.accs.length > 0">
                <v-list-subheader>Awards</v-list-subheader>
                <v-list-item
                  v-for="acc in submission.accs"
                  :key="acc.accId"
                  :value="formatAward(submission, acc)"
                  active-color="primary"
                >
                  <v-list-item-title
                    v-text="formatAward(submission, acc)"
                  ></v-list-item-title>
                </v-list-item>
              </v-list>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
    <v-spacer></v-spacer>

    <NewAuthorDialog
      v-model:visible="newAuthorDialogVisible"
      :pcode="pcode"
    ></NewAuthorDialog>
  </v-container>
</template>
<script lang="ts" setup>
import { FsValidationResult } from "vue-file-selector/dist";
import { useRoute } from "vue-router";
import { ref, type Ref, onMounted, watch } from "vue";
import {
  Project,
  dummyProject,
  Submission,
  Award,
  Publication,
} from "@/types/project";
import {
  loadProject,
  loadSubmissions,
  updateProject,
  removeStudent,
  deleteProject,
} from "@/api/projects";
import names from "@/util/names";
import wordCount from "@/util/wordCount";
import PDFViewer from "pdf-viewer-vue";
import { useAppStore } from "@/store/app";

import default_image from "@/assets/default.png";

import NewAuthorDialog from "@/components/newAuthor/NewAuthorDialog.vue";
import { useRouter } from "vue-router";

const router = useRouter();
const appStore = useAppStore();
const ownProject = ref(true);
const route = useRoute();

const pcode = ref("");

const project: Ref<Project> = ref(dummyProject());

const tempAbstract = ref("");
const tempTitle = ref("");
const editAbstract = ref(false);
const editTitle = ref(false);

const submissions: Ref<Submission[]> = ref([]);

const newAuthorDialogVisible = ref(false);

watch(newAuthorDialogVisible, (dialog: boolean, prevDialog: boolean) => {
  /* ... */
  if (!dialog && prevDialog) {
    // Falling Edge lol
    loadProject(pcode.value).then((res) => {
      project.value = res;
      tempAbstract.value = res.abstract;
      ownProject.value =
        project.value.members.filter(
          (member) => member.email == appStore.user?.email,
        ).length > 0;
    });
    loadSubmissions(pcode.value).then((res) => {
      submissions.value = res;
    });
  }
});

function updateGeneralProject() {
  updateProject(
    project.value.pcode,
    project.value.title,
    project.value.abstract,
    project.value.reportPdf,
  ).then((res) => (project.value = res ?? project.value));
}

function updateAbstract() {
  project.value.abstract = tempAbstract.value.trim() || ""; // remove leading and trailing spaces from tempAbstract
  updateGeneralProject();
}

function updateTitle() {
  project.value.title = tempTitle.value.trim() || "";
  updateGeneralProject();
}

function removeMember(email: string) {
  removeStudent(email, project.value.pcode).then(
    (res) => (project.value = res ?? project.value),
  );
}

async function deleteEntireProject() {
  if (await deleteProject(pcode.value)) router.push("/projects");
}

function formatAward(submission: Submission, acc: Award | Publication) {
  if ("name" in acc) {
    // Award
    if (acc.prize.length > 0) return `🏆 ${acc.name} (${acc.prize})`;
    else return acc.name;
  } else {
    return `📰 Publication in ${submission.eventId} ${submission.year}`;
  }
}

function handleFilesValidated(result: FsValidationResult, files: File[]) {
  // console.log('Validation result: ' + result);
}

function getBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      resolve(reader.result as string);
    };
    reader.onerror = (error) => {
      // error reading file, or other error
      reject(error); // or simply ignore the error
    };
  });
}

function handleFilesChanged(files: File[]) {
  const newReport = files[0];

  getBase64(newReport).then((res) => {
    project.value.reportPdf = res.substring(28);
    updateGeneralProject();
  });
}

onMounted(() => {
  pcode.value = route.params.id as string;
  loadProject(pcode.value).then((res) => {
    project.value = res;
    tempAbstract.value = res.abstract;
    ownProject.value =
      project.value.members.filter(
        (member) => member.email == appStore.user?.email,
      ).length > 0;
  });
  loadSubmissions(pcode.value).then((res) => {
    submissions.value = res;
  });
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

.v-textarea .v-field {
  font-size: 0.875rem;
}

.v-text-field .v-field {
  font-size: 20px;
}

.titleEdit {
  display: none;
}

.ptitle:hover + .titleEdit {
  display: block;
}

.v-list-item:hover {
  active-color: primary;
}
</style>
