<template>
  <div>
    <Row>
        <Col span="4">
          <div>
            <span>{{info}}</span>
          </div>
        </Col>
      <Col span="20">
          <DatePicker type="date" :options="datePickerOption" placeholder="请选择时间" @on-change="updateInfo"
          style="width: 200px;height: 40px;padding-bottom: 10px;float: right;"></DatePicker>
      </Col>
    </Row>
    <Row :gutter="20">
      <i-col :xs="12" :md="8" :lg="4" v-for="(infor, i) in inforCardData" :key="`infor-${i}`" style="height: 120px;padding-bottom: 10px;">
        <infor-card shadow :color="infor.color" :icon="infor.icon" :icon-size="36">
          <div>
            <span style="font-size: 38px;">{{ infor.count }}</span>
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
          <chart-pie style="height: 300px;" :value="cash_flow_in_reasons" text="今日营业消费额"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="summary_sell_money" text="今日净入账"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="hairdresser_sell_number" text="今日发型师营业额"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="assistant_sell_number" text="今日助理营业额"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="24" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="week_sell_numbers" text="近30天营业消费额"/>
        </Card>
      </i-col>
      <i-col :md="24" :lg="24" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="week_sell_money" text="近30天净收入"/>
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
import Example from './example.vue'
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
        { title: '开单数量', icon: 'md-locate', count: 0, color: '#19be6b' },
        { title: '会员消费次数', icon: 'md-help-circle', count: 0, color: '#ff9900' },
        { title: '营业消费额', icon: 'md-share', count: 0, color: '#ed3f14' },
        { title: '净入账', icon: 'md-chatbubbles', count: 0, color: '#E46CBB' },
        { title: '净支出', icon: 'md-map', count: 0, color: '#9A66E4' }
      ],
      sell_money_items_type: [],
      sell_item_type: [],
      cash_flow_in_reasons: [],
      hairdresser_sell_number: [],
      assistant_sell_number: [],
      summary_sell_money: [],
      week_sell_numbers: {},
      week_sell_money: {},
      info: '如下为今日的数据统计',
      datePickerOption: {
        shortcuts: [
          {
            text: '今天',
            value () {
              return new Date();
            },
            onClick: (picker) => {
              // this.$Message.info('选择今天');
            }
          },
          {
            text: '昨天',
            value () {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              return date;
            },
            onClick: (picker) => {
              // this.$Message.info('选择昨天');
            }
          },
          {
            text: '一周前',
            value () {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              return date;
            },
            onClick: (picker) => {
              // this.$Message.info('选择一周前');
            }
          }
        ]
      }
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
      var post_URL = baseAPIUrl + 'get_daily_data/' + date
      console.log(post_URL)
      this.$http.get(post_URL).then(response => {
        const res = response.data
        this.inforCardData[0]['count'] = res['data']['new_count_fellow']
        this.inforCardData[1]['count'] = res['data']['items_count']
        this.inforCardData[2]['count'] = res['data']['fellow_item_count']
        this.inforCardData[3]['count'] = res['data']['sell_number']
        this.inforCardData[4]['count'] = res['data']['sell_money']
        this.inforCardData[5]['count'] = res['data']['cost']
        this.sell_money_items_type = res['data']['sell_money_items_type']
        this.sell_item_type = res['data']['sell_item_type']
        this.cash_flow_in_reasons = res['data']['cash_flow_in_reasons']

        this.hairdresser_sell_number = res['data']['hairdresser_sell_number']
        this.assistant_sell_number = res['data']['assistant_sell_number']
        this.summary_sell_money = res['data']['summary_sell_money']

        this.week_sell_numbers = res['data']['week_sell_numbers']
        this.week_sell_money = res['data']['week_sell_money']
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
        this.info = '如下为今日的数据分析'
      }
      else {
        this.info = '如下为 ' + date + ' 的数据分析'
      }
      this.getDailyData(date)
    }
  }
}
</script>
