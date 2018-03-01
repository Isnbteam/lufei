<template>
  <div>
    <h3>课程</h3>
    <h4>项目实战 你的同行都在学</h4>
    <span>更全面的实战案例、更细致的讲解和课后辅导，让你的职业生涯能更轻松的完成进阶</span>
    <ul>
      <li  class="aa" v-for="item in courseList">
        <router-link :to="{'path':'/course-detail/'+item.id }">
          <img v-bind:src="item.course_img">
          <div>{{item.name}}</div>
          <div>{{item.brief}}</div>
          <div>难度：{{item.level}}</div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    name: 'course',
    data () {
      return {
        courseList: []
      }
    },
    mounted: function () {
      this.initCourses()
    },
    methods: {
      initCourses: function () {
        var that = this
        this.$axios.request({
          url: 'http://127.0.0.1:8000/courses/',
          method: 'GET'
        }).then(function (response) {
          that.courseList = response.data.courseList
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.aa{
  display: inline;
}
</style>
