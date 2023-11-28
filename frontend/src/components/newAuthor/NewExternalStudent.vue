<template>
  <v-card-text>
    If your friend isn't in our database (i.e. he isn't a NUSH Student), you can
    register him here. <br />
    <br />

    Please insert all these details and we will register him, in addition to
    adding him to this project.
  </v-card-text>
  <v-container fluid>
    <v-form fast-fail @submit.prevent>
      <v-row>
        <v-col cols="12" sm="6" xs="12" md="6">
          <v-text-field
            label="Email"
            v-model="studentEmail"
            :rules="emailRules"
            prepend-inner-icon="mdi-email-outline"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" xs="12" md="6">
          <v-text-field
            label="Name"
            v-model="studentName"
            :rules="nameRules"
            hint="Insert Full Name"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" xs="12" md="6">
          <v-text-field
            label="Teacher Email"
            v-model="teacherEmail"
            :rules="emailRules"
            prepend-inner-icon="mdi-email-outline"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" xs="12" md="6">
          <v-text-field
            label="Teacher Name"
            v-model="teacherName"
            :rules="nameRules"
            hint="Insert Full Name"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" xs="12" md="6">
          <v-select
            :items="schools"
            label="Institute"
            prepend-inner-icon="mdi-book-education-outline"
            item-title="name"
            item-value="instId"
            v-model="school"
            :hint="school ? `${school?.name} (${school?.instId})` : ''"
            return-object
            single-line
            persistent-hint
            required
          ></v-select>
        </v-col>
        <v-col cols="12" sm="6" xs="12" md="6">
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              :loading="submitLoading"
              color="primary"
              size="large"
              type="submit"
              @click="submit()"
              variant="elevated"
              >Add</v-btn
            >
          </v-card-actions>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { School } from "@/types/admin";
import { searchSchools } from "@/api/institutes";
import { createExternalStudent } from "@/api/user";
import { addStudents } from "@/api/projects";

export default defineComponent({
  props: {
    pcode: { type: String, required: true },
  },
  data: () => ({
    school: null as School | null,
    schools: [] as School[],
    studentEmail: "",
    studentName: "",
    teacherEmail: "",
    teacherName: "",
    emailRules: [
      (value: string | null) => {
        if (value?.match(/^[a-z.-_]+@[a-z.-]+(\.[a-z]+)+$/i)) return true;
        return "Please enter a valid email.";
      },
    ],
    nameRules: [
      (value: string | null) => {
        if ((value?.length ?? 0) >= 3) return true;
        return "The name should consider at least 3 characters.";
      },
    ],
    submitLoading: false,
  }),
  methods: {
    async submit() {
      this.submitLoading = true;
      await createExternalStudent(
        this.studentEmail,
        this.studentName,
        this.teacherEmail,
        this.teacherName,
        this.school!!.instId,
      );
      await addStudents([this.studentEmail], this.pcode);
      this.submitLoading = false;
    },
  },
  async mounted() {
    this.schools = await searchSchools();
  },
});
</script>
