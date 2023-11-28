<template>
  <v-dialog v-model="value" persistent fullscreen width="100%">
    <v-card class="mx-auto pa-auto">
      <v-toolbar color="primary">
        <template v-slot:prepend> </template>
        <v-toolbar-title> Submit to Event </v-toolbar-title>

        <v-spacer></v-spacer>
        <v-btn variant="text" icon="mdi-close" @click="value = false"></v-btn>
      </v-toolbar>

      <div class="mx-4">
        <v-container fluid>
          <v-form fast-fail @submit.prevent>
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  label="Submission Code"
                  v-model="code"
                  :rules="codeRules"
                  hint="Code allocated to you (e.g. BE023). If none is provided, input your project code."
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="8">
                <v-autocomplete
                  v-model="projects"
                  :disabled="isProjectUpdating"
                  :items="allProjects"
                  chips
                  closable-chips
                  item-title="title"
                  item-value="pcode"
                  label="Select Projects"
                  multiple
                  hide-selected
                  return-object
                >
                  <template v-slot:chip="{ props, item }">
                    <v-chip v-bind="props" :text="item.raw.pcode"></v-chip>
                  </template>

                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="item?.raw?.title"
                      :subtitle="item?.raw?.pcode"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col cols="12" md="6">
                <v-combobox
                  label="Submission Title"
                  v-model="subTitle"
                  :rules="titleRules"
                  :items="projects.map((it) => it.title)"
                  hint=""
                  required
                ></v-combobox>
              </v-col>
              <v-col cols="12" md="6">
                <v-autocomplete
                  v-model="authors"
                  v-model:search="search"
                  :disabled="isStudentUpdating"
                  :items="searchedStudents"
                  chips
                  closable-chips
                  item-title="name"
                  item-value="email"
                  label="Select Authors"
                  multiple
                  hide-selected
                  return-object
                >
                  <template v-slot:chip="{ props, item }">
                    <v-chip
                      v-bind="props"
                      :prepend-avatar="`data:image/png;base64,${item.raw.pfp}`"
                      :text="item.raw.name"
                    ></v-chip>
                  </template>

                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :prepend-avatar="`data:image/png;base64,${item.raw.pfp}`"
                      :title="item?.raw?.name"
                      :subtitle="item?.raw?.email"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  clearable
                  auto-grow
                  v-model="subAbstract"
                  clear-icon="mdi-close-circle"
                  label="Submission Abstract"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    :loading="submitLoading"
                    color="primary"
                    size="large"
                    type="submit"
                    @click="submit()"
                    variant="elevated"
                    >Create</v-btn
                  >
                </v-card-actions>
              </v-col>
            </v-row>
          </v-form>
        </v-container>
      </div>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { ResearchEvent } from "@/types/project";
import { defineComponent } from "vue";
import { User } from "@/types/user";
import fuzzysort from "fuzzysort";

import { useAppStore } from "@/store/app";

import { loadStudents } from "@/api/user";
import { loadProjects, createSubmission } from "@/api/projects";

import { Project } from "@/types/project";

export default defineComponent({
  props: {
    visible: { type: Boolean, required: true },
    event: { type: ResearchEvent, required: true },
  },
  emits: {
    "update:visible": null,
  },
  computed: {
    value: {
      get(): boolean {
        return this.visible;
      },
      set(value: boolean) {
        this.$emit("update:visible", value);
      },
    },
    search: {
      get(): string {
        return this.query;
      },

      set(search: string) {
        if (this.query !== search) {
          this.query = search;

          this.searchedStudents = (
            search.length == 0
              ? this.students
              : fuzzysort
                  .go(search, this.students, { keys: ["email", "name"] })
                  .map((it) => it.obj)
          ).slice(0, 5);
        }
      },
    },
  },
  data: () => ({
    query: "",
    allProjects: [] as Project[],
    projects: [] as Project[],
    authors: [] as User[],
    searchedStudents: [] as User[],
    students: [] as User[],
    isStudentUpdating: false,
    isProjectUpdating: false,
    studentTimeout: null as any,
    projectTimeout: null as any,
    appStore: useAppStore(),
    code: "",
    codeRules: [
      (value: string | null) => {
        if ((value?.length ?? 0) >= 3) return true;
        return "The code should consider at least 3 characters.";
      },
    ],
    titleRules: [
      (value: string | null) => {
        if ((value?.length ?? 0) >= 3) return true;
        return "The title should consider at least 3 characters.";
      },
    ],
    submitLoading: false,
    subTitle: "",
    subAbstract: "",
  }),
  watch: {
    isProjectUpdating(val) {
      clearTimeout(this.projectTimeout);

      if (val) {
        this.projectTimeout = setTimeout(
          () => (this.isProjectUpdating = false),
          3000,
        );
      }
    },
    isStudentUpdating(val) {
      clearTimeout(this.studentTimeout);

      if (val) {
        this.studentTimeout = setTimeout(
          () => (this.isStudentUpdating = false),
          3000,
        );
      }
    },
  },
  methods: {
    async submit() {
      this.submitLoading = true;
      await createSubmission(
        this.event.eventId,
        this.event.year,
        this.code,
        this.subTitle,
        this.subAbstract,
        this.projects.map((it) => it.pcode),
        [this.appStore.user.email, ...this.authors.map((it) => it.email)],
      );
      this.value = false;
      this.submitLoading = false;
    },
  },
  async mounted() {
    this.students = await loadStudents();
    this.allProjects = await loadProjects(this.appStore.user.email);
  },
});
</script>
