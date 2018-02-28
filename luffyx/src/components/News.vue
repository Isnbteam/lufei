<template>
  <div>
    <ul>
      <li v-for="item in courseList" class="news-item-wrap">
        <router-link :to="{'path':'/newsDetail/'+item.id}">
          <div style="width: 282px; height: 159px; overflow: hidden" >
            <img v-bind:src="item.head_img" alt="">
          </div>
          <div class="info">
            <span>{{item.title}}</span><br>
            <span>点赞数：{{item.agree_num}}</span>
            <span>收藏数：{{item.collect_num}}</span>
            <span>评论数：{{item.comment_num}}</span>
            <span>观看数：{{item.view_num}}</span><br>
            <span>摘要：{{item.brief}}</span><br>
            <span>#{{item.source.name}}#</span>
          </div>
        </router-link>
        <hr>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      courseList:[]
    }
  },
  mounted: function () {
    this.initCourses()
  },
  methods: {
    initCourses:function () {
      var that = this
      this.$axios.request({
        url: 'http://127.0.0.1:8000/news/',
        method: 'GET'
      }).then(function (response) {
        that.courseList = response.data
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
