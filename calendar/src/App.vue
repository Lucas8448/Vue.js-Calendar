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
    <input type="radio" :id="day" :value="day.name" name="day" v-model="CurrentDay">
    <label :for="day" v-bind:class="{ 'calendar-today': day.name === CurrentDay }" @click="GetDate(day.date)">{{ day.name
      }}</label>
  </template>
</div>
    <!--A dropdown with all countries where CurrentCountries gets updated with the selected value-->
<div class="countries">
  <select v-model="CurrentCountry">
        <option v-for="country in countries" :key="country" :value="country">{{ country.name }}</option>
  </select>
</div>
</div>
<form @submit.prevent="addEvent">
  <label for="eventTitle">Event Title:</label>
  <input type="text" v-model="eventTitle" id="eventTitle" required />
  <br />
  <label for="eventDescription">Event Description:</label>
  <input type="text" v-model="eventDescription" id="eventDescription" required />
  <br />
  <label for="eventStart">Event Start:</label>
  <input type="date" v-model="eventStart" id="eventStart" required />
  <br />
  <label for="eventEnd">Event End:</label>
  <input type="date" v-model="eventEnd" id="eventEnd" required />
  <br />
  <label for="eventColour">Event Colour:</label>
  <input type="color" v-model="eventColour" id="eventColour" required />
  <br />
  <button type="submit">Add Event</button>
</form>
<ul>
  <li v-for="event in events" :key="event.event_id">
    <p>Title: {{ event.event_title }}</p>
    <p>Description: {{ event.event_description }}</p>
    <p>Start time: {{ event.event_start }}</p>
    <p>End time: {{ event.event_end }}</p>
    <p>Colour: {{ event.event_colour }}</p>
  </li>
</ul>
</template>

<script>
import countriesList from 'countries-list';

const API_URL = `http://localhost:5174`

export default {
  data: () => ({
    countries: Object.values(countriesList.countries),
    CurrentCountry: countriesList.countries["NO"],
    days: "",
    CurrentDay: "",
    weeks: Array.from({ length: 52 }, (_, i) => i + 1),
    CurrentWeek: "",
    CurrentDate: "",
    CurrentDay: "",
    events: ""
  }),

  created() {
    // fetch on init
    this.GetToday()
    this.Events()
  },
  methods: {
    async GetToday() {
      this.resp = await (await (await fetch(`${API_URL}/goto/today`)).json())
      this.days = this.resp.week,
      this.CurrentDate = this.resp.date,
      this.CurrentDay = this.resp.day,
      this.CurrentWeek = this.resp.weekNum
      console.log("Page loaded")
      console.log(this.resp)
    },
    async GetDate(date) {
      if (this.CurrentDate === date) {
        return;
      }
      this.resp = await (await (await fetch(`${API_URL}/goto/${date}`)).json())
      this.days = this.resp.week,
      this.CurrentDate = this.resp.date,
      this.CurrentDay = this.resp.day,
      this.CurrentWeek = this.resp.weekNum
      console.log("Date changed")
      console.log(this.resp)
    },
    async Events() {
      this.events = await (await (await fetch(`${API_URL}/events/${this.CurrentDate}`)).json())
      console.log("Events loaded")
      console.log(this.events)
    },
    async addEvent() {
      // Make a POST request to the server with the event details
      const response = await fetch(`${API_URL}/events/add/${this.eventTitle}/${this.eventDescription}/${this.eventStart}/${this.eventEnd}`)
      // Check the response status to see if the event was successfully added
      if (response.status === 200) {
        // Event was successfully added
        console.log("Event added successfully")
      } else {
        // There was an error adding the event
        console.error("Error adding event")
      }
    },
  }
}
</script>
