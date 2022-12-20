<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="nav">
  <div class="weekTitle">

    <h1>Week {{ CurrentWeek }}</h1>
  </div>

<h2 class="currentDate">{{ CurrentDate }}</h2>
<div class="days">
  <template v-for="day in days">
    <input type="radio" :id="day" :value="day" name="day" v-model="CurrentDay" @click="GetDay()">
    <label :for="day">{{ day }}</label>
  </template>
</div>
    <!--A dropdown with all countries where CurrentCountries gets updated with the selected value-->
<div class="countries">
  <select v-model="CurrentCountry">
        <option v-for="country in countries" :key="country" :value="country">{{ country.name }}</option>
  </select>
</div>
</div>
</template>

<script>
import countriesList from 'countries-list';

const API_URL = `http://localhost:5174/`

export default {
  data: () => ({
    countries: Object.values(countriesList.countries),
    days: "",
    weeks: Array.from({ length: 52 }, (_, i) => i + 1),
    CurrentDay: "",
    CurrentWeek: "",
    CurrentDate: "",
    CurrentCountry: countriesList.countries["NO"],
    commits: null
  }),

  created() {
    // fetch on init
    this.GetToday()
  },
  methods: {
    async GetToday() {
      this.resp = await (await (await fetch(`${API_URL}today`)).json())
      this.CurrentDate = this.resp.date,
        this.days = this.resp.days,
        this.CurrentDay = this.resp.weekday,
      this.CurrentWeek = this.resp.week
    },
    async GetDate() { 
      this.resp = await (await (await fetch(`${API_URL}goto/date/${this.CurrentDate}`)).json())
      this.day_data = this.resp
      this.CurrentDay = this.day_data.weekday
      this.CurrentWeek = this.day_data.week
      this.CurrentDate = this.day_data.date
    },
    async GetWeek() {
      this.resp = await (await (await fetch(`${API_URL}goto/week/${this.CurrentWeek}`)).json())
      this.day_data = this.resp
      this.CurrentDay = this.day_data.weekday
      this.CurrentWeek = this.day_data.week
      this.CurrentDate = this.day_data.date
    },
    async GetDay() {
      this.resp = await (await (await fetch(`${API_URL}goto/day/${this.CurrentDay}/${this.CurrentDate}`)).json())
      this.day_data = this.resp
      this.CurrentDay = this.day_data.weekday
      this.CurrentWeek = this.day_data.week
      this.CurrentDate = this.day_data.date
    }
  }
}
</script>
