<template>
  <div>
    <h3>帮助有志向的年轻人通过努力学习
      获得体面的工作和生活</h3>

      <div class="aa" v-for="item in degreecourseList">
        <router-link :to="{'path':'/course-detail/'+item.id }">
          <img v-bind:src="item.course_img">
          <div>先修知识：{{item.prerequisite}}</div>
          <div>{{item.name}}</div>
          <div>{{item.brief}}</div>
          <div>课程详情>>></div>
        </router-link>
      </div>

  </div>
</template>

<script>
  export default {
    name: 'degreeCourse',
    data () {
      return {
        degreecourseList: []
      }
    },
    mounted: function () {
      this.initdegreecourse()
    },
    methods: {
      initdegreecourse: function () {
        var that = this
        this.$axios.request({
          url: 'http://127.0.0.1:8000/degreecourse/',
          method: 'GET'
        }).then(function (response) {
          console.log(response.data.degreecourseList)
          that.degreecourseList = response.data.degreecourseList
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .aa {
    display: inline-block;
    border: 1px solid red;
    width: 350px;
    height: 200px;
    margin-left: 50px;
  }
</style>
