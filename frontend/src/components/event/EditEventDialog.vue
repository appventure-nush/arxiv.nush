<template>
  <v-dialog
    v-model="value"
    persistent
    fullscreen
    width="100%"
  >
    <v-card class="mx-auto pa-auto">

  <v-toolbar color="primary">
    <v-toolbar-title>
      Edit Research Event
    </v-toolbar-title>
    <v-spacer/>
    <v-btn variant="text" icon="mdi-close" @click="value = false"></v-btn>
  </v-toolbar>
      <div class="mx-4">
        <v-container fluid>
          <v-form fast-fail @submit.prevent>
            <v-row>
              <v-col cols="12" sm="12" md="8">
                <v-text-field label="Event Name" v-model="eventName"
                  :rules="nameRules"
                  hint="Insert Full Event Name" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <div class="d-flex">
                <v-text-field label="Event Abbreviation" disabled v-model="eventId"
                  :rules="nameRules"
                  hint="Insert Event Abbreviation" required></v-text-field>
                <v-text-field label="Event Year" disabled v-model="eventYear"
                  :rules="numberRules"
                  hint="Insert Event Year" required></v-text-field>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  :items="formatOptions" label="Format" prepend-inner-icon="mdi-book-education-outline"
                  hint="Format of Event"
                  v-model="format" single-line persistent-hint required></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <VueDatePicker v-model="dates" :enable-time-picker="false" range></VueDatePicker>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-autocomplete
                  v-model="searchedOrganisers"
                  :disabled="isUpdating"
                  :items="organisers"
                  chips
                  closable-chips
                  item-title="name"
                  item-value="instId"
                  label="Select"
                  multiple
                  hide-selected
                  return-object>
                  <template v-slot:chip="{ props, item }">
                    <v-chip
                      v-bind="props"
                      :text="item.raw.name"
                    ></v-chip>
                  </template>

                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="item?.raw?.name"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col cols="12" sm="6" md="4">

                <v-autocomplete
                  v-model="eventType"
                  :items="eventTypeOptions"
                  chips closable-chips
                  hide-details
                  hide-no-data
                  hide-selected
                  label="Competition Type" v-on:keydown.enter.prevent=""
                  multiple
                  single-line
                ></v-autocomplete>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-combobox
                  v-if="eventType.includes('Competition')"
                  v-model="awardTypes"
                  :items="[]"
                  label="Award Types" v-on:keydown.enter.prevent=""
                  multiple
                  chips closable-chips
                ></v-combobox>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field label="Conference DOI (Optional)" v-model="confDoi"
                  v-if="eventType.includes('Conference')"
                  hint="Conference DOI"></v-text-field>
              </v-col>
              <v-col cols="12" v-model="about">
                <MdEditor language="en-US" v-model="about"></MdEditor>

              </v-col>
              <v-col cols="12">
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn :loading="submitLoading"
                    color="primary" size="large"
                    type="submit" @click="submit()"
                    variant="elevated">Edit</v-btn>
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
import { defineComponent } from 'vue'
import { loadStudents } from '@/api/user'
import { User } from '@/types/user'
import fuzzysort from 'fuzzysort'
import { searchOrganisers } from "@/api/institutes"
import {GeneralInstitute} from "@/types/admin"
import { addStudents } from "@/api/projects"
import { sub } from 'date-fns'

import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { ResearchEvent } from '@/types/project'
import {updateEvent} from "@/api/events"

import MdEditor from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';

export default defineComponent({
  // type inference enabled
  props: {
    visible: { type: Boolean, required: true },
    event: { type: ResearchEvent, required: true }
  },
  emits: {
    'update:visible': null,
    'update:event': null
  },
  components: { VueDatePicker, MdEditor },
  computed: {
    value: {
      get(): boolean {
        return this.visible
      },
      set(value: boolean) {
        this.$emit('update:visible', value)
      }
    },
    eventValue: {
      get(): ResearchEvent {
        return this.event
      },
      set(value: ResearchEvent) {
        this.$emit('update:event', value)
      }
    }
  },
  watch: {
    value(newValue, oldValue) {
      if(newValue == true) {
        this.eventName = this.event.name
        this.eventYear = this.event.year
        this.eventId = this.event.eventId
        this.about = this.event.about
        this.eventType = this.event.isConference && this.event.isCompetition ? ['Conference', 'Competition'] : this.event.isConference ? ["Conference"] : this.event.isCompetition ? ["Competition"] : []
        this.format = this.event.format
        this.awardTypes = this.event.awardTypes
        this.dates = [this.event.start_date, this.event.end_date]
        this.format = this.event.format
        this.confDoi = this.event.confDoi ?? ""
        this.searchedOrganisers = this.event.organisers as GeneralInstitute[]
      }
    }
  },
  data() {
    return {
      autoUpdate: true,
      timeout: null as any,
      submitLoading: false,
      organisers: [] as GeneralInstitute[],
      formatOptions: ["Virtual", "IRL", "Hybrid"],
      eventTypeOptions: ["Competition", "Conference"],
      eventName: this.event.name,
      eventYear: this.event.year,
      eventId: this.event.eventId,
      about: this.event.about,
      eventType: this.event.isConference && this.event.isCompetition ? ['Conference', 'Competition'] : this.event.isConference ? ["Conference"] : this.event.isCompetition ? ["Competition"] : [],
      awardTypes: this.event.awardTypes,
      dates: [this.event.start_date, this.event.end_date],
      format: this.event.format,
      confDoi: this.event.confDoi ?? "",
      searchedOrganisers: this.event.organisers as GeneralInstitute[],
      isUpdating: false,
      nameRules: [
        (value: string | null) => {
          if((value?.length ?? 0) >= 3) return true
          return "The name should consider at least 3 characters."
        }
      ],
      numberRules: [
        (value: string) => {
          if(value.match(/^[0-9]+$/)) return true;
          return "Year should be numeric."
        }
      ]
    }
  },
  methods: {
    dateToString(date: Date) {
      return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`
    },
    async submit() {
      this.submitLoading = true;
      const event = await updateEvent(
        this.eventId, this.eventYear, this.eventName, this.dateToString(this.dates[0]),
        this.dates.length > 1 ? this.dateToString(this.dates[1]) : this.dateToString(this.dates[0]),
        this.format, this.about, this.eventType.includes("Competition"), this.eventType.includes("Conference"),
        this.searchedOrganisers.map(it => it.instId), this.awardTypes, this.confDoi
      )
      this.submitLoading = false;
      this.value = false;
      this.eventValue = event;
    }
  },
  async mounted() {
    this.organisers = await searchOrganisers()
    this.eventName = this.event.name
    this.eventYear = this.event.year
    this.eventId = this.event.eventId
    this.about = this.event.about
    this.eventType = this.event.isConference && this.event.isCompetition ? ['Conference', 'Competition'] : this.event.isConference ? ["Conference"] : this.event.isCompetition ? ["Competition"] : []
    this.format = this.event.format
    this.awardTypes = this.event.awardTypes
    this.dates = [this.event.start_date, this.event.end_date]
    this.format = this.event.format
    this.confDoi = this.event.confDoi ?? ""
    this.searchedOrganisers = this.event.organisers as GeneralInstitute[]
  }
})
</script>
