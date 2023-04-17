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

        <v-tabs
      v-model="tab"
      fixed-tabs
      bg-color="primary"
    >
      <v-tab value="one">Add Members</v-tab>
      <v-tab value="two">Register Members</v-tab>
    </v-tabs>
      </template>
      <v-spacer/>
      <v-btn variant="text" icon="mdi-close" @click="value = false"></v-btn>
    </v-toolbar>


        <!-- <v-card-text> -->
            <!-- <v-row class="mx-4"> -->
              <!-- <v-col cols="6"> -->

      <v-window v-model="tab">
        <v-window-item value="one" class="mx-4">
                <v-card-text>
                  Start typing to find your teammates.

                </v-card-text>
                <!-- <v-card-title>Add new members!</v-card-title> -->
                <v-autocomplete
                  v-model="authors"
                  v-model:search="search"
                  :disabled="isUpdating"
                  :items="searchedStudents"
                  chips
                  closable-chips
                  item-title="name"
                  item-value="email"
                  label="Select"
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
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary"
                    variant="elevated"
                    @click="addMembers();"
                    :loading="manyAddLoading">Add</v-btn>
                </v-card-actions>
                </v-window-item>

                <v-window-item value="two" class="mx-4">
              <NewExternalStudent :pcode="pcode"></NewExternalStudent>
          </v-window-item>
          </v-window>
      </v-card>
    </v-dialog>

</template>
<script lang="ts">
import { defineComponent } from 'vue'
import { loadStudents } from '@/api/user'
import { User } from '@/types/user'
import fuzzysort from 'fuzzysort'
import { searchSchools } from "@/api/institutes"
import {GeneralInstitute} from "@/types/admin"
import { addStudents } from "@/api/projects"

import NewExternalStudent from './NewExternalStudent.vue'

export default defineComponent({
  // type inference enabled
  props: {
    visible: { type: Boolean, required: true },
    pcode: { type: String, required: true }
  },
  components: {
    NewExternalStudent
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
  data() {
    return {
      autoUpdate: true,
      isUpdating: false,
      authors: [] as User[],
      searchedStudents: [] as User[],
      students: [] as User[],
      timeout: null as any,
      query: '',
      schools: [] as GeneralInstitute[],
      school: null as (GeneralInstitute | null),
      tab: null as any,
      manyAddLoading: false,
      singleAddLoading: false
    }
  },
  watch: {
    isUpdating (val) {
      clearTimeout(this.timeout)

      if (val) {
        this.timeout = setTimeout(() => (this.isUpdating = false), 3000)
      }
    },
  },
  methods: {
    async addMembers() {
      const members = this.authors.map(it => it.email);
      this.manyAddLoading = true;
      await addStudents(members, this.pcode);
      this.authors = [];
      this.manyAddLoading = false;
    }
  },
  async mounted() {
    this.students = await loadStudents()
    this.schools = await searchSchools()
  }
})
</script>
