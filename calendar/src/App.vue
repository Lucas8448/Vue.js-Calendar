<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <h1>Calendar</h1>
  <template v-for="day in days" class="nav">
    <input type="radio" :id="day" :value="day" name="day" v-model="CurrentDay">
    <label :for="day">{{ day }}</label>
  </template>
  <h3>{{ CurrentDay }}</h3>
  <ul>

  </ul>
</template>

<style>
.nav {
  display: inline-block;
  margin-right: 1em;
  text-align: center;
  align-items: center;
}

input[type="radio"] {
  display: none;
}

input[type="radio"] + label {
  display: inline-block;
  padding: 0.5em 1em;
  margin: 0 0.5em 0.5em 0;
  border: 1px solid #ccc;
  border-radius: 0.25em;
  cursor: pointer;
}
</style>

<script>
const API_URL = `http://localhost:5000/`

export default {
  data: () => ({
    days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    weeks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52],
    CurrentDay: "",
    CurrentWeek: "",
    Date: "",
    commits: null
  }),

  created() {
    // fetch on init
    this.UpdateCurrentDay(),
    this.UpdateCurrentWeek(),
    this.GetDay()
  },
  methods: {
    async UpdateCurrentDay() {
      this.resp = await (await (await fetch(`${API_URL}get/day`)).json())
      this.CurrentDay = this.resp
      console.log(this.CurrentDay)
    },
    async UpdateCurrentWeek() {
      this.resp = await (await (await fetch(`${API_URL}get/week`)).json())
      this.CurrentWeek = this.resp
      console.log(this.CurrentWeek)
    },
    async GetDay() {
      if (typeof this.CurrentWeek !== "undefined" || typeof this.CurrentDay !== "undefined") {
        this.resp = await (await (await fetch(`${API_URL}day/${this.CurrentWeek}/${this.CurrentDay}`)).json())
        this.date = this.resp
        console.log(this.date)
      }
      else {
        setTimeout(this.GetDay(), 20);
      }
    }
  }
}
</script>
