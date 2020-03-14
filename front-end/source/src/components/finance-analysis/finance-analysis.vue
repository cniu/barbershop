/* eslint-disable camelcase */
<template>
  <div>
    <Row>
        <Col span="4">
          <div>
            <span>{{info}}</span>
          </div>
        </Col>
        <Col span="16">
            <DatePicker type="year" placeholder="请选择年份" @on-change="updateInfo"
            style="width: 200px;height: 40px;padding-bottom: 10px; float:right;"></DatePicker>
        </Col>
        <Col span="4">
            <DatePicker type="month" placeholder="请选择月份" @on-change="updateInfo"
            style="width: 200px;height: 40px;padding-bottom: 10px; float:right;"></DatePicker>
        </Col>
    </Row>
    <Row :gutter="20">
      <i-col :xs="12" :md="8" :lg="4" v-for="(infor, i) in inforCardData" :key="`infor-${i}`" style="height: 120px;padding-bottom: 10px;">
        <infor-card shadow :color="infor.color" :icon="infor.icon" :icon-size="36">
          <div>
            <span style="font-size: 35px;">{{ infor.count }}</span>
          </div>
          <p>{{ infor.title }}</p>
        </infor-card>
      </i-col>
    </Row>
    <Row :gutter="20" style="margin-top: 10px;">
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="sell_money_items_type" text="客户开单付款类别"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="sell_item_type" text="客户开单服务类别"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="cash_flow_in_reasons" text="营业消费额"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="24" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="year_sell_numbers" text="今年营业消费额"/>
        </Card>
      </i-col>
      <i-col :md="24" :lg="24" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="year_sell_money" text="今年净收入"/>
        </Card>
      </i-col>
    </Row>
<!--     <Row>
      <Card shadow>
        <example style="height: 310px;"/>
      </Card>
    </Row> -->
  </div>
</template>
<script type="text/javascript">
import { ChartPie, ChartBar } from '../charts'
import Example from './history.vue'
import InforCard from '@/components/info-card'
const baseAPIUrl = process.env.baseAPIUrl
export default {
  name: 'Dashboard',
  components: {
    ChartPie,
    ChartBar,
    Example,
    InforCard
  },
  data () {
    return {
      inforCardData: [
        { title: '新增会员', icon: 'md-person-add', count: 0, color: '#2d8cf0' },
        { title: '开单总数', icon: 'md-locate', count: 0, color: '#19be6b' },
        { title: '会员消费次数', icon: 'md-help-circle', count: 0, color: '#ff9900' },
        { title: '营业消费额', icon: 'md-share', count: 0, color: '#ed3f14' },
        { title: '净入账', icon: 'md-chatbubbles', count: 0, color: '#E46CBB' },
        { title: '净支出', icon: 'md-map', count: 0, color: '#9A66E4' },
        { title: '当前会员卡金剩余', icon: 'md-map', count: 0, color: '#E46CBB' },
        { title: '当前会员总数', icon: 'md-map', count: 0, color: '#2d8cf0' }
      ],
      sell_money_items_type: [],
      sell_item_type: [],
      cash_flow_in_reasons: [],
      year_sell_numbers: {},
      year_sell_money: {},
      info: '如下信息为今年的数据分析'
    }
  },
  created: function () {
  },
  mounted () {
    this.$nextTick(() => {
      this.getDailyData('now')
    })
  },
  methods: {
    getDailyData (date) {
      var post_URL = baseAPIUrl + 'get_all_data/' + date

      this.$http.get(post_URL).then(response => {
        const res = response.data
        this.inforCardData[0]['count'] = res['data']['new_count_fellow']
        this.inforCardData[1]['count'] = res['data']['items_count']
        this.inforCardData[2]['count'] = res['data']['fellow_item_count']
        this.inforCardData[3]['count'] = res['data']['sell_number']
        this.inforCardData[4]['count'] = res['data']['sell_money']
        this.inforCardData[5]['count'] = res['data']['cost']
        this.inforCardData[6]['count'] = res['data']['fellow_rest_money']
        this.inforCardData[7]['count'] = res['data']['fellow_sum_count']
        this.sell_money_items_type = res['data']['sell_money_items_type']
        this.sell_item_type = res['data']['sell_item_type']
        this.cash_flow_in_reasons = res['data']['cash_flow_in_reasons']
        this.year_sell_numbers = res['data']['year_sell_numbers']
        this.year_sell_money = res['data']['year_sell_money']
        if (res['status'] != 'success') { this.$Message.error(res['message']) }
      }, response => {
        if (response.status == 401) {
          // this.$Message.error('请登陆');
          this.$router.push({
            name: 'login'
          })
        }
      })
    },
    updateInfo (date) {
      if (date === '') {
        date = 'now'
        this.info = '如下为今年的数据分析'
      }
      else {
        this.info = '如下为 ' + date + ' 的数据分析'
      }
      this.getDailyData(date)
    }
  }
}
</script>
