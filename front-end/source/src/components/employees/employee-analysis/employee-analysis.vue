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
          <chart-pie style="height: 300px;" :value="sell_item_type" text="客户开单服务类别"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="hairdresser_sell_number" text="发型师营业额"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="assistant_sell_number" text="助理营业额"></chart-pie>
        </Card>
      </i-col>
    </Row>
    <Row :gutter="20">
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;" v-for="(info, i) in employee_analysis_result" :key="`info-${i}`">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="info.content" :text="info.name"></chart-pie>
        </Card>
      </i-col>
    </Row>
      
      <!-- <i-col :md="24" :lg="24" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="year_sell_numbers" text="今年营业消费额"/>
        </Card>
      </i-col>
      <i-col :md="24" :lg="24" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="year_sell_money" text="今年净收入"/>
        </Card>
      </i-col> -->
<!--     <Row>
      <Card shadow>
        <example style="height: 310px;"/>
      </Card>
    </Row> -->
  </div>
</template>
<script type="text/javascript">
import { ChartPie, ChartBar } from '../../charts'
import InforCard from '@/components/info-card'
const baseAPIUrl = process.env.baseAPIUrl
export default {
  name: 'Dashboard',
  components: {
    ChartPie,
    ChartBar,
    InforCard
  },
  data () {
    return {
      inforCardData: [
        { title: '开单总数', icon: 'md-locate', count: 0, color: '#19be6b' },
        { title: '营业额（仅开单）', icon: 'md-share', count: 0, color: '#ed3f14' },
        { title: '均价（仅开单）', icon: 'md-chatbubbles', count: 0, color: '#ff9900' }
      ],
      sell_item_type: [],
      assistant_sell_number: [],
      hairdresser_sell_number: [],
      employee_analysis_result: [],
      info: '如下信息为当月的数据分析'
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
      var post_URL = baseAPIUrl + 'get_employee_data/' + date

      this.$http.get(post_URL).then(response => {
        const res = response.data
        this.inforCardData[0]['count'] = res['data']['items_count']
        this.inforCardData[1]['count'] = res['data']['sell_number']
        this.inforCardData[2]['count'] = 0
        if (res['data']['items_count'] != 0){
          this.inforCardData[2]['count'] = (res['data']['sell_number'] / res['data']['items_count']).toFixed(2)
        }

        this.sell_item_type = res['data']['sell_item_type']
        this.hairdresser_sell_number = res['data']['hairdresser_sell_number']
        this.assistant_sell_number = res['data']['assistant_sell_number']

        this.employee_analysis_result = res['data']['employee_analysis_result']
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
        this.info = '如下为当月的数据分析'
      }
      else {
        this.info = '如下为 ' + date + ' 的数据分析'
      }
      this.getDailyData(date)
    }
  }
}
</script>
