<template>
  <v-dialog
    v-model="value"
    persistent
    fullscreen
    width="100%"
  >
    <v-card class="mx-auto pa-auto">
      <v-toolbar color="primary">
        <template v-slot:prepend>

        </template>
        <v-toolbar-title>
          Create new Project
        </v-toolbar-title>

        <v-spacer></v-spacer>
      <v-btn variant="text" icon="mdi-close" @click="value = false"></v-btn>

      </v-toolbar>

      <div class="mx-4">
        <v-container fluid>
          <v-form fast-fail @submit.prevent>
            <v-row>
              <v-col cols='12' md="6">
                <div class="d-flex">
                <v-text-field label="Project Code" v-model="code"
                  :rules="codeRules" @update:model-value="computeSubject()"
                  hint="Code allocated to you (e.g. 23.NUSH.018.CS)" required></v-text-field>
                <v-text-field label="Year" v-model="year"
                  :rules="yearRules"
                  hint="Year that project is presented." required></v-text-field>
                <v-combobox
                    label="Department"
                    :items="['BI', 'CM', 'CS', 'EL', 'HU', 'MA', 'PH', 'RE']"
                    clearable @update:search="computedSubject = false"
                    v-model="deptSearch"
                  ></v-combobox>
                </div>
              </v-col>
              <v-col cols='12' md="6">
                <v-text-field label="Project Title" v-model="title"
                  :rules="titleRules" hint="Title of Project" required></v-text-field>
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
                  return-object>
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

              <v-col cols='12' md="6">

                <v-autocomplete
                  v-model="teacher"
                  :items="teachers"
                  item-title="name"
                  item-value="email"
                  label="Select Teacher Mentor"
                  return-object>
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
                            v-model = "abstract"
                            clear-icon="mdi-close-circle"
                            label="Abstract"
                        ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn :loading="submitLoading"
                    color="primary" size="large"
                    type="submit" @click="submit()"
                    variant="elevated">Create</v-btn>
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
import { defineComponent } from 'vue';
import { User, dummyTeacher } from '@/types/user';
import fuzzysort from 'fuzzysort';

import { useAppStore } from '@/store/app';
import { useRouter } from 'vue-router';

import { loadStudents, loadTeachers } from '@/api/user';
import { loadProjects, createProject } from '@/api/projects';

import { Project } from '@/types/project';


export default defineComponent({
  props: {
    visible: { type: Boolean, required: true }
  },
  emits: {
    'update:visible': null
  },
  computed: {
    value: {
      get(): boolean {
        return this.visible
      },
      set(value: boolean) {
        this.$emit('update:visible', value)
      }
    },
    search: {
      get (): string  {
        return this.query
      },

      set (search: string) {
        if (this.query !== search) {
          this.query = search

          this.searchedStudents = (search.length == 0 ? this.students : fuzzysort.go(search, this.students, { keys : ['email', 'name']}).map(it => it.obj)).slice(0, 5)
        }
      }
    }
  },
  data: () => ({
    query: '',
    allProjects: [] as Project[],
    projects: [] as Project[],
    authors: [] as User[],
    searchedStudents: [] as User[],
    students: [] as User[],
    teachers: [] as User[],
    teacher: dummyTeacher(),
    isStudentUpdating: false,
    isProjectUpdating: false,
    studentTimeout: null as any,
    projectTimeout: null as any,
    appStore: useAppStore(),
    router: useRouter(),
    code: "",
    computedSubject: false,
    year: (new Date()).getFullYear(),
    title: "",
    codeRules: [
      (value: string | null) => {
        if((value?.length ?? 0) < 14) return "The code should contain at least 14 characters."
        if((value?.length ?? 0) > 20) return "The code should contain 20 or less characters."
        return true
      }
    ],
    yearRules: [
      (value: number | null) => {
        if((value ?? 0) < 2006) return "The project should have been presented after 2005."
        if((value ?? 0) > 2099) return "The project should have been presented in the 21st Century."
      }
    ],
    titleRules: [
      (value: string | null) => {
        if((value?.length ?? 0) < 3) return "The title should consider at least 3 characters."
        if((value?.length ?? 0) > 200) return "The title should be shorter than 200 characters."
        return true
      }
    ],
    submitLoading: false,
    abstract: "",
    deptSearch: ""
  }),
  watch: {
    isProjectUpdating (val) {
      clearTimeout(this.projectTimeout)

      if (val) {
        this.projectTimeout = setTimeout(() => (this.isProjectUpdating = false), 3000)
      }
    },
    isStudentUpdating (val) {
      clearTimeout(this.studentTimeout)

      if (val) {
        this.studentTimeout = setTimeout(() => (this.isStudentUpdating = false), 3000)
      }
    },
  },
  methods: {
    async submit() {
      this.submitLoading = true;
      await createProject(
        this.code, this.year, this.deptSearch.length == 2 ? this.deptSearch : "RE",
        this.title, this.abstract, this.teacher.email,
        [this.appStore.user.email, ...this.authors.map(it => it.email)]
      )
      this.value = false;
      this.submitLoading = false;
      this.router.push(`/projects/${this.code}`)
    },
    computeSubject() {
      const subj = this.code.split(".")[this.code.replace(/[^.]/g, "").length].toUpperCase()
      if(['BI', 'CM', 'CS', 'EL', 'HU', 'MA', 'PH', 'RE'].includes(subj) && (this.computedSubject || (this.deptSearch.length == 0))) {
        this.deptSearch = subj;
        this.computedSubject = true;
      }
    }
  },
  async mounted() {
    this.students = await loadStudents()
    this.teachers = await loadTeachers()
    this.allProjects = await loadProjects(this.appStore.user.email)
  }
})

</script>
