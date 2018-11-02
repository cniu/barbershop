<template>
    <div>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="8">
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
    </div>
</template>
<script>
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "FellowConsumptions",
    data () {
        return {
            search: '',
            page: 1,
            page_size: 20,
            total_count: 0,
            order: "desc",
            order_key: "created_time",
            items_data: [],
            columns: [
                {
                    title: '编号',
                    key: 'raw_id',
                    width: 80
                },
                {
                    title: '会员手机号',
                    key: 'phone_number',
                    sortable: 'custom'
                },
                {
                    title: '会员卡类型',
                    key: 'card_type',
                    sortable: 'custom'
                },
                {
                    title: '消费金额',
                    key: 'expend_money',
                    sortable: 'custom'
                },
                {
                    title: '余额',
                    key: 'remain_money',
                    sortable: 'custom'
                },
                {
                    title: '消费单号',
                    key: 'sell_item_number',
                    sortable: 'custom'
                },
                {
                    title: '消费原因',
                    key: 'reason',
                    sortable: 'custom'
                },
                {
                    title: '记录时间',
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
    created: function() {
        this.getItems();
    },
    methods: {
        getItems() {
            var post_URL = baseAPIUrl + "fellow_money_history?";
            post_URL += "page=" + this.page;
            post_URL += "&page_size=" + this.page_size;
            post_URL += "&order=" + this.order;
            post_URL += "&order_key=" + this.order_key;

            this.$http.post(post_URL, {search: this.search}).then(response => {
                const res = response.data;
                this.items_data = res['data'];
                this.total_count = res['total_count'];
                this.page = res['page'];
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
        },
        handleSearch(value) {
            this.search = value;
            this.getItems();
        },
        changePage(page) {
            this.page = page;
            this.getItems();
        },
        changePageSize(page_size) {
            this.page_size = page_size;
            this.getItems();
        },
        sortChange(value){
            this.order = value.order;
            this.order_key = value.key;
            this.getItems();
        }
    }
}
</script>
