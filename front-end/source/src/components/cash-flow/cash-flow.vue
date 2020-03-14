<template>
    <div>
        <Row type="flex" justify="end" class="code-row-bg" style="padding: 10px;">
            <Col span="4">
                <Button type="primary" shape="circle" @click="addItem">添加其他出账入账记录</Button>
            </Col>
            <Col span="8" offset="12">
                <Input search enter-button placeholder="请输入关键字搜索" style="width: 300px;float: right;" @on-search="handleSearch" v-model="search"/>
            </Col>
        </Row>
        <Row type="flex" justify="start" class="code-row-bg" style="padding: 10px;">
            <Col span="24">
                <Table border :columns="columns" :data="items_data" @on-sort-change="sortChange"></Table>
            </Col>
        </Row>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="24">
                <Page :total="total_count" show-total show-sizer :current="page" :page-size="page_size" :page-size-opts=[20,50,100,500] @on-change="changePage" @on-page-size-change="changePageSize" style="float: right;"/>
            </Col>
        </Row>
        <Modal
            v-model="singleModal" footer-hide
            :title="modal_title">
            <AddFlow :singleItem="singleItem" :modal_type="modal_type" @closeModal="closeModal" :employee_list="employee_list"></AddFlow>
        </Modal>
    </div>
</template>
<script>
import AddFlow from './in-out.vue'
const baseAPIUrl = process.env.baseAPIUrl
export default {
  name: 'CashFlow',
  components: {
    AddFlow
  },
  data () {
    return {
      singleItem: {},
      modal_type: 'add',
      modal_title: '添加其他出账入账记录',
      singleModal: false,
      employee_list: '',
      search: '',
      page: 1,
      page_size: 20,
      total_count: 0,
      order: 'desc',
      order_key: 'created_time',
      items_data: [],
      columns: [
        {
          title: '编号',
          key: 'raw_id',
          width: 80
        },
        {
          title: '资金变动类别',
          key: 'reason',
          sortable: 'custom'
        },
        {
          title: '消费单号',
          key: 'sell_item_number',
          sortable: 'custom'
        },
        {
          title: '金额',
          key: 'money',
          sortable: 'custom'
        },
        {
          title: '金额流向',
          key: 'flow_direction',
          sortable: 'custom'
        },
        {
          title: '备注',
          key: 'comment',
          sortable: 'custom'
        },
        {
          title: '开单时间',
          key: 'created_time',
          sortable: 'custom'
        }
      ]
    }
  },
  computed: {
  },
  watch: {
  },
  created: function () {
    this.getItems()
    this.getEmployees()
  },
  methods: {
    getItems () {
      var post_URL = baseAPIUrl + 'cash_flow?'
      post_URL += 'page=' + this.page
      post_URL += '&page_size=' + this.page_size
      post_URL += '&order=' + this.order
      post_URL += '&order_key=' + this.order_key

      this.$http.post(post_URL, {search: this.search}).then(response => {
        const res = response.data
        this.items_data = res['data']
        this.total_count = res['total_count']
        this.page = res['page']
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
    getEmployees () {
      var post_URL = baseAPIUrl + 'summarized_employees'

      this.$http.get(post_URL).then(response => {
        const res = response.data
        this.employee_list = res['employee_list']
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
    handleSearch (value) {
      this.search = value
      this.getItems()
    },
    changePage (page) {
      this.page = page
      this.getItems()
    },
    changePageSize (page_size) {
      this.page_size = page_size
      this.getItems()
    },
    sortChange (value) {
      this.order = value.order
      this.order_key = value.key
      this.getItems()
    },
    addItem () {
      this.modal_type = 'add'
      this.modal_title = '添加其他出账入账记录'
      this.singleItem = {}
      this.singleModal = true
      this.getItems()
    },
    closeModal (text) {
      this.singleModal = false
      this.getItems()
    }
  }
}
</script>
