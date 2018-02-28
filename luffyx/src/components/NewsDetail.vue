<template>
  <div>
    <h3>{{title}}</h3>
        <span>点赞：{{agree_num}}</span>
        <span>收藏：{{collect_num}}</span>
        <span>评论：{{comment_num}}</span>
        <span>阅读：{{view_num}}</span>
    <br>
    <p>{{content}}</p>
    <div>
       <span>#{{source}}#</span>
       <button @click="agree">点赞|{{agree_num}}</button>
       <button @click="collect">收藏|{{collect_num}}</button>
    </div>
    <p><input type="text" placeholder="评论" value="" disabled="disabled"><button>提交</button></p>

  </div>
</template>

<script>
export default {
  data () {
    return {
      comment_list: [],
      title:'',
      content: '',
      agree_num:'',
      collect_num:'',
      comment_num:'',
      view_num:'',
      source:'',
      agree_sta:false,
      collect_sta: false
    }
  },

  mounted: function () {
    this.initNewsDetail ()
  },

  methods: {
    initNewsDetail (){
      var nid = this.$route.params.id
      var that = this
      var url = 'http://127.0.0.1:8000/news/' + nid + '.json'
      this.$axios.request({
        url: url,
        method: 'GET',
        responseType: 'json'
      }).then(function (response) {
        console.log(response)
        that.title = response.data.title
        that.content = response.data.content
        that.agree_num = response.data.agree_num
        that.collect_num = response.data.collect_num
        that.view_num = response.data.view_num
        that.comment_num = response.data.comment_num
        that.source = response.data.source.name
      })
    },
    //点赞
    agree () {
      var that = this
      if (!this.agree_sta) {
        that.agree_num = that.agree_num + 1
        console.log(that.agree_num)
        var article_id = this.$route.params.id
        var url = 'http://127.0.0.1:8000/news/' + article_id + '.json'
        this.$axios.request({
          url: url,
          method: 'PUT',
          params: {
            article_id: article_id,
            agree_num: that.agree_num,
            agree_info: 'True'
          },
          responseType: 'json'  // 响应的格式
        }).then(function (response) {
          console.log(response)
        })
      } else {
        that.agree_num = that.agree_num - 1
        var article_id = this.$route.params.id
        var url = 'http://127.0.0.1:8000/news/' + article_id + '.json'
        this.$axios.request({
          url: url,
          method: 'PUT',
          params: {
            article_id: article_id,
            agree_num: that.agree_num,
            agree_info: ''
          },
          responseType: 'json'// 响应的格式
        }).then(function (response) {
          console.log(response)
        })
      }
      this.agree_sta = !this.agree_sta
    },
    // 收藏
    collect () {
      var that = this
      if (!this.collect_sta) {
        that.collect_num = that.collect_num + 1
        console.log(that.collect_num)
        var article_id = this.$route.params.id
        var url = 'http://127.0.0.1:8000/micro/' + article_id + '.json'
        this.$axios.request({
          url: url,
          method: 'PUT',
          params: {
            article_id: article_id,
            collect_num: that.collect_num,
            collect: 'collect',
            collect_msg: 'collect'
          },
          responseType: 'json'// 响应的格式
        }).then(function (response) {
          console.log(response)
          alert(response.data.msg)
        })
      } else {
        that.collect_num = that.collect_num - 1
        console.log(that.collect_num)
        var article_id = this.$route.params.id
        var url = 'http://127.0.0.1:8000/micro/' + article_id + '.json'
        this.$axios.request({
          url: url,
          method: 'PUT',
          params: {
            article_id: article_id,
            collect_num: that.collect_num,
            collect: '',
            collect_msg: 'collect'
          },
          responseType: 'json'// 响应的格式
        }).then(function (response) {
          console.log(response)
          alert(response.data.msg)
        })
      }
      this.collect_sta = !this.collect_sta
    },
    // 评论


  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
