<template>
    <div>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="8">
                <Input search enter-button placeholder="请输入关键字搜索" style="width: 300px;float: right;" @on-search="handleSearch" v-model="search"/>
            </Col>
        </Row>
        <Row type="flex" justify="start" class="code-row-bg" style="padding: 10px;">
            <Col span="24">
                <Table border :columns="columns" :data="sell_items_data" @on-sort-change="sortChange"></Table>
            </Col>
        </Row>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="24">
                <Page :total="total_count" show-total show-sizer :current="page" :page-size="page_size" :page-size-opts=[20,50,100,500] @on-change="changePage" @on-page-size-change="changePageSize" style="float: right;"/>
            </Col>
        </Row>
        <Modal
            v-model="singleModal" footer-hide
            title="修改单子"
            @on-visible-change="visibleChange">
            <SellItem :singleItem="singleItem" :modal_type="modal_type" @closeModal="closeModal" :hairdresser_list="hairdresser_list" :assistant_list="assistant_list" :fellow_list="fellow_list"></SellItem>
        </Modal>
    </div>
</template>
<script>
import SellItem from './sell-item.vue'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "SellItems",
    components: {
        SellItem
    },
    data () {
        return {
            singleItem: {},
            modal_type: "modify",
            singleModal: false,
            search: '',
            page: 1,
            page_size: 20,
            total_count: 0,
            order: "desc",
            order_key: "created_time",
            sell_items_data: [],
            assistant_list: [],
            hairdresser_list: [],
            fellow_list: [],
            columns: [
                {
                    title: '编号',
                    key: 'raw_id',
                    width: 80
                },
                {
                    title: '单号',
                    key: 'item_number',
                    sortable: 'custom'
                },
                {
                    title: '发型师',
                    key: 'hairdresser',
                    sortable: 'custom'
                },
                {
                    title: '助理',
                    key: 'assistant',
                    sortable: 'custom'
                },
                {
                    title: '消费类型',
                    key: 'item_type',
                    sortable: 'custom'
                },
                {
                    title: '金额',
                    key: 'money',
                    sortable: 'custom'
                },
                {
                    title: '付款类型',
                    key: 'pay_type',
                    sortable: 'custom'
                },
                {
                    title: '会员',
                    key: 'fellow',
                    sortable: 'custom'
                },
                {
                    title: '备注',
                    key: 'comment',
                    ellipsis: true,
                    sortable: 'custom'
                },
                {
                    title: '开单时间',
                    key: 'created_time',
                    sortable: 'custom'
                },
                {
                    title: 'Action',
                    key: 'action',
                    width: 150,
                    align: 'center',
                    render: (h, params) => {
                        return h('div', [
                            h('Button', {
                                props: {
                                    type: 'primary',
                                    size: 'small'
                                },
                                style: {
                                    marginRight: '5px'
                                },
                                on: {
                                    click: () => {
                                        this.modifyItem(params.index)
                                    }
                                }
                            }, '编辑'),
                            h('Button', {
                                props: {
                                    type: 'error',
                                    size: 'small'
                                },
                                on: {
                                    click: () => {
                                        this.removeItem(params.index)
                                    }
                                }
                            }, '删除')
                        ]);
                    }
                }
            ]
        }
    },
    computed: {
    },
    watch: {
    },
    created: function() {
        this.getSellItems();
        this.getEmployees();
        this.getFellows();
    },
    methods: {
        getSellItems() {
            var post_URL = baseAPIUrl + "sell_items?";
            post_URL += "page=" + this.page;
            post_URL += "&page_size=" + this.page_size;
            post_URL += "&order=" + this.order;
            post_URL += "&order_key=" + this.order_key;

            this.$http.post(post_URL, {search: this.search}).then(response => {
                const res = response.data;
                this.sell_items_data = res['data'];
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
        getEmployees() {
            var post_URL = baseAPIUrl + "summarized_employees";

            this.$http.get(post_URL).then(response => {
                const res = response.data;
                this.hairdresser_list = res['hairdresser_list'];
                this.assistant_list = res['assistant_list'];
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
        getFellows() {
            var post_URL = baseAPIUrl + "summarized_fellows";

            this.$http.get(post_URL).then(response => {
                const res = response.data;
                this.fellow_list = res['response_list'];
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
            this.getSellItems();
        },
        show (index) {
            this.$Modal.info({
                title: 'User Info',
                content: `Name：${this.sell_items_data[index].name}<br>Age：${this.sell_items_data[index].age}<br>Address：${this.sell_items_data[index].address}`
            })
        },
        modifyItem(index) {
            this.singleModal = true;
            this.singleItem = Object.assign({}, this.sell_items_data[index]);
            this.singleItem['item_type'] = this.singleItem['item_type'].split(',');
        },
        removeItem(index) {
            this.$Modal.confirm({
                title: '是否确认删除',
                content: '',
                onOk: () => {
                    var post_URL = baseAPIUrl + "sell_item/" + this.sell_items_data[index].item_number;

                    this.$http.delete(post_URL).then(response => {
                        const res = response.data;
                        if(res['status'] != "success")
                            this.$Message.error(res['message']);

                        this.$Message.success('删除成功!');
                        this.getUsers();
                    }, response => {
                        if(response.status == 403){
                            this.$Message.error('权限不足，请申请权限');
                            // this.$router.push({
                            //     name: "dashboard"
                            // });
                        }
                        else if(response.status == 401){
                          // this.$Message.error('请登陆');
                          this.$router.push({
                            name: "login"
                          });
                        }
                    });
                },
                onCancel: () => {
                    // this.$Message.info('Clicked cancel');
                }
            });
        },
        changePage(page) {
            this.page = page;
            this.getSellItems();
        },
        changePageSize(page_size) {
            this.page_size = page_size;
            this.getSellItems();
        },
        sortChange(value){
            this.order = value.order;
            this.order_key = value.key;
            this.getSellItems();
        },
        visibleChange(status) {
            this.singleModal = status;
        },
        closeModal(text) {
            this.singleModal = false;
            this.getSellItems();
        }
    }
}
</script>
