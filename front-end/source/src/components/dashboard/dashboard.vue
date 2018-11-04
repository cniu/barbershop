<template>
  <div>
    <Row :gutter="20">
      <i-col :xs="12" :md="8" :lg="4" v-for="(infor, i) in inforCardData" :key="`infor-${i}`" style="height: 120px;padding-bottom: 10px;">
        <infor-card shadow :color="infor.color" :icon="infor.icon" :icon-size="36">
          <div>
            <span style="font-size: 50px;">{{ infor.count }}</span>
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
          <chart-pie style="height: 300px;" :value="cash_flow_in_reasons" text="营业额"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="24" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="week_sell_numbers" text="近七天营业额"/>
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
const baseAPIUrl = process.env.baseAPIUrl;
import { ChartPie, ChartBar } from '../charts'
import Example from './example.vue'
import InforCard from '@/components/info-card'
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
        { title: '今日新增会员', icon: 'md-person-add', count: 0, color: '#2d8cf0' },
        { title: '今日开单数量', icon: 'md-locate', count: 0, color: '#19be6b' },
        { title: '会员消费次数', icon: 'md-help-circle', count: 0, color: '#ff9900' },
        { title: '今日消费总额', icon: 'md-share', count: 0, color: '#ed3f14' },
        { title: '今日净入账', icon: 'md-chatbubbles', count: 0, color: '#E46CBB' },
        { title: '今日净支出', icon: 'md-map', count: 0, color: '#9A66E4' }
      ],
      sell_money_items_type: [],
      sell_item_type: [],
      cash_flow_in_reasons: [],
      week_sell_numbers: {}
    }
  },
  created: function(){
  },
  mounted () {
    this.$nextTick(() => {
      this.getDailyData();
    });
  },
  methods: {
      getDailyData() {
          var post_URL = baseAPIUrl + "get_daily_data";

          this.$http.get(post_URL).then(response => {
              const res = response.data;
              this.inforCardData[0]['count'] = res['data']['new_count_fellow'];
              this.inforCardData[1]['count'] = res['data']['items_count'];
              this.inforCardData[2]['count'] = res['data']['fellow_item_count'];
              this.inforCardData[3]['count'] = res['data']['sell_number'];
              this.inforCardData[4]['count'] = res['data']['sell_money'];
              this.inforCardData[5]['count'] = res['data']['cost'];
              this.sell_money_items_type = res['data']['sell_money_items_type'];
              this.sell_item_type = res['data']['sell_item_type'];
              this.cash_flow_in_reasons = res['data']['cash_flow_in_reasons'];
              this.week_sell_numbers = res['data']['week_sell_numbers'];
              if(res['status'] != "success")
                  this.$Message.error(res['message']);
          }, response => {
              if(response.status == 401){
                // this.$Message.error('请登陆');
                this.$router.push({
                  name: "login"
                });
              }
          });
      }
    }
}
</script>