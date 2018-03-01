<template>
  <div>
    <div>学位课程详情</div>
    <div>
      <div style="float: left;margin-left: 180px">
        <img v-bind:src="degreecourse.course_img">
      </div>
      <div style="float: right;margin-right: 180px">
        <div v-for="i in courseList">
          <h3>{{i.name}}({{i.level}})￥{{i.price}}起</h3>
          <p>{{i.brief}}</p>

        </div>
        <div style="float: left">
          <button>入群免费试听</button>
        </div>
        <div style="float: right">点击左侧按钮，扫码加入课程交流QQ群。
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  export default {
    name: 'degreeourseDetail',
    data () {
      return {
        degreecourse: '',
        courseList: [],

      }
    },
    mounted: function () {
      this.initCourseDetail()
    },
    methods: {

    initCourseDetail (){
      var nid = this.$route.params.id
      var that = this
      var url = 'http://127.0.0.1:8000/degreecourse/' + nid + '.json'
      this.$axios.request({
        url: url,
        method: 'GET',
        responseType: 'json'
      }).then(function (response) {
        console.log(response.data)
        that.degreecourse = response.data.degreecourse
        that.courseList = response.data.courseList

      })
    }
  }
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #qh li {
    list-style: none;
    display: inline-block;
    border: 1px solid #b7b4ed;
    height: 40px;
    line-height: 40px;
    width: 120px;
    margin-left: 40px;

    text-align: center;
  }

  #price li {
    list-style: none;
    display: inline-block;
    border: 1px solid #b7b4ed;
    height: 80px;
    line-height: 80px;
    width: 150px;
    margin-left: 30px;
    text-align: center;
  }

  .gs {
    margin-left: 15px;
  }
</style>
