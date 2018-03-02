<template>
  <div>
    <div>专题课程</div>
    <h1>{{course.name}}</h1>
    <span>{{course_slogan}}</span>
    <div>
      <ul id="qh">
        <li><span v-on:click="qh(1)">课程概述</span></li>
        <li><span v-on:click="qh(2)">课程章节</span></li>
        <li><span v-on:click="qh(3)">用户评价</span></li>
        <li><span v-on:click="qh(4)">常见问题</span></li>
      </ul>
      <div v-show="a[0]">
        <h2>课程概述</h2>
        <p>{{video_brief_link}}</p>
        <span class="gs">学习时间：{{hours}}小时</span>
        <span class="gs">难度：{{course.level}}</span>
        <span class="gs">学习人数：0人</span>
        <div>
          <div id="price" v-for="price in course.prices">


            <div>￥{{price.price}}
              有效期{{price.valid_period}}
            </div>


          </div>
          <div>
            <button>开课时通知我</button>
          </div>
        </div>
        <h2>为什么学这门课程</h2>
        <p>{{why_study}}</p>
        <h2>我将学到哪些内容？</h2>
        <p>{{what_to_study_brief}}</p>
        <h2>此项目如何有助于我的职业生涯？</h2>
        <p>{{career_improvement}}</p>
        <h2>课程先修要求</h2>
        <p>{{prerequisite}}</p>
        <h2>推荐课程</h2>
        <p>若你缺乏相关经验，建议学习以下课程</p>
        <ul>
          <li v-for="row in courses.recommend" @click="recommendCourse(row.id)"><h4>{{row.name}}</h4></li>
        </ul>
        <h2>讲师简介</h2>
        <div v-for="item in teachers">
          <h3>{{item.name}}、{{item.title}}</h3>
          <img v-bind:src="item.image">
          <span>{{item.signature}}</span>
          <p>{{item.brief}}</p>

        </div>
      </div>
      <div v-show="a[1]">
        <h2>课程章节</h2>
        <div>
          <ul>
            <li v-for="i in coursechapterList">
              <h3>第{{i.chapter}}章&nbsp;{{i.name}}</h3>
              <ul>
                <li v-for="s in i.coursesections">
                  <a href="">{{s.name}}<span style="float: right">{{s.video_time}}</span></a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
      <div v-show="a[2]">
        <div style="height: 100px;width: 100%">
          <h2>热评推荐</h2>
        </div>
        <div style="height: 100px;width: 100%">
          <h2>全部评论</h2>
        </div>
      </div>
      <div v-show="a[3]">
        <h2>常见问题</h2>
        <ul>
          <li v-for="d in oftenaskedquestion">
            <h3>{{d.question}}</h3>
            <p>{{d.answer}}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>

</template>

<script>
  export default {
      name:'course-detail',
    data () {
      return {
        courseId: this.$route.params.id,
        courses: '',
        selectCourseIndex: -1,
        course: '',
        hours: '',
        course_slogan: '',
        video_brief_link: '',
        why_study: '',
        what_to_study_brief: '',
        career_improvement: '',
        prerequisite: '',
        teachers: [],
        oftenaskedquestion: [],
        a: [1, 0, 0, 0],
        coursechapterList: [],
      }
    },
    mounted: function () {
      this.initCourseDetail()
    },
    methods: {
      qh: function (t) {
        if (t == 2) {
          this.a = [0, 1, 0, 0]
        } else if (t == 3) {
          this.a = [0, 0, 1, 0]
        } else if (t == 4) {
          this.a = [0, 0, 0, 1]

        } else if (t == 1) {
          this.a = [1, 0, 0, 0]
        }
      },
      initCourseDetail (){
        var courseId=this.courseId
        var that = this
        var url = this.$store.state.apiList.courses + courseId + '.json'
        this.$axios.request({
          url: url,
          method: 'GET',
          responseType: 'json'
        }).then(function (response) {
          that.course = response.data.course
          that.courses = response.data.courses
          that.hours = response.data.courses.hours
          that.oftenaskedquestion = response.data.courses.oftenaskedquestion
          that.course_slogan = response.data.courses.course_slogan
          that.why_study = response.data.courses.why_study
          that.what_to_study_brief = response.data.courses.what_to_study_brief
          that.career_improvement = response.data.courses.career_improvement
          that.prerequisite = response.data.courses.prerequisite
          that.video_brief_link = response.data.courses.video_brief_link
          that.teachers = response.data.courses.teachers
          that.coursechapterList = response.data.coursechapterList
        })
      },
      recommendCourse: function (courseId) {
        this.$router.push({name: 'course-detail', params: {id: courseId}})
        this.courseId = courseId
        this.initCourseDetail()
      },
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

  #price {
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
