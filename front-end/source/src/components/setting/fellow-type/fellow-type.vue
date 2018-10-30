<template>
    <div>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="8">
                <Input search enter-button placeholder="请输入关键字搜索" style="width: 300px;float: right;" @on-search="handleSearch" v-model="search"/>
            </Col>
        </Row>
        <Row type="flex" justify="start" class="code-row-bg" style="padding: 10px;">
            <Col span="24">
                <Table border :columns="columns" :data="fellow_type_data" @on-sort-change="sortChange"></Table>
            </Col>
        </Row>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="24">
                <Page :total="total_count" show-total show-sizer :current="page" :page-size="page_size" :page-size-opts=[20,50,100,500] @on-change="changePage" @on-page-size-change="changePageSize" style="float: right;"/>
            </Col>
        </Row>
        <Modal
            v-model="singleModal" footer-hide
            title="修改类别"
            @on-visible-change="visibleChange">
            <FellowType :singleItem="singleItem" :modal_type="modal_type" @closeModal="closeModal"></FellowType>
        </Modal>
    </div>
</template>
<script>
import FellowType from './sell-item.vue'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "FellowTypeManage",
    components: {
        FellowType
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
            fellow_type_data: [],
            columns: [
                {
                    title: '编号',
                    key: 'raw_id',
                    width: 80
                },
                {
                    title: '会员卡类型名称',
                    key: 'card_type_name',
                    sortable: 'custom'
                },
                {
                    title: '打折比率',
                    key: 'discount',
                    sortable: 'custom'
                },
                {
                    title: '备注',
                    key: 'comment',
                    ellipsis: true,
                    sortable: 'custom'
                },
                {
                    title: '更新时间',
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
        this.getFellowTypes();
    },
    methods: {
        getFellowTypes() {
            var post_URL = baseAPIUrl + "setting/fellow_types?";
            post_URL += "page=" + this.page;
            post_URL += "&page_size=" + this.page_size;
            post_URL += "&order=" + this.order;
            post_URL += "&order_key=" + this.order_key;

            this.$http.post(post_URL, {search: this.search}).then(response => {
                const res = response.data;
                this.fellow_type_data = res['data'];
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
            this.getFellowTypes();
        },
        modifyItem(index) {
            this.singleModal = true;
            this.singleItem = Object.assign({}, this.fellow_type_data[index]);
        },
        changePage(page) {
            this.page = page;
            this.getFellowTypes();
        },
        changePageSize(page_size) {
            this.page_size = page_size;
            this.getFellowTypes();
        },
        sortChange(value){
            this.order = value.order;
            this.order_key = value.key;
            this.getFellowTypes();
        },
        visibleChange(status) {
            this.singleModal = status;
        },
        closeModal(text) {
            this.singleModal = false;
            this.getFellowTypes();
        },
        removeItem() {

        }
    }
}
</script>
