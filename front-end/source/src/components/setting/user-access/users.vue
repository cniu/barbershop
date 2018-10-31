<template>
    <div>
        <Row type="flex" justify="end" class="code-row-bg" style="padding: 10px;">
            <Col span="4">
                <Button type="primary" shape="circle" @click="addItem">添加</Button>
            </Col>
            <Col span="8" offset="12">
                <Input search enter-button placeholder="请输入关键字搜索" style="width: 300px;float: right;" @on-search="handleSearch" v-model="search"/>
            </Col>
        </Row>
        <Row type="flex" justify="start" class="code-row-bg" style="padding: 10px;">
            <Col span="24">
                <Table border :columns="columns" :data="users_data" @on-sort-change="sortChange"></Table>
            </Col>
        </Row>
        <Row type="flex" justify="end" class="code-row-bg" style="padding: 10px;">
            <Col span="24">
                <Page :total="total_count" show-total show-sizer :current="page" :page-size="page_size" :page-size-opts=[20,50,100,500] @on-change="changePage" @on-page-size-change="changePageSize" style="float: right;"/>
            </Col>
        </Row>
        <Modal
            v-model="singleModal" footer-hide
            :title="modal_title"
            @on-visible-change="visibleChange">
            <User :singleItem="singleItem" :modal_type="modal_type" @closeModal="closeModal"></User>
        </Modal>
    </div>
</template>
<script>
import User from './sell-item.vue'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "UserManage",
    components: {
        User
    },
    data () {
        return {
            singleItem: {},
            modal_type: "modify",
            modal_title: "",
            singleModal: false,
            search: '',
            page: 1,
            page_size: 20,
            total_count: 0,
            order: "desc",
            order_key: "created_time",
            users_data: [],
            columns: [
                {
                    title: '编号',
                    key: 'raw_id',
                    width: 80
                },
                {
                    title: '登陆用户用户名',
                    key: 'username',
                    sortable: 'custom'
                },
                {
                    title: '权限级别',
                    key: 'page_level',
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
        this.getUsers();
    },
    methods: {
        getUsers() {
            var post_URL = baseAPIUrl + "setting/users?";
            post_URL += "page=" + this.page;
            post_URL += "&page_size=" + this.page_size;
            post_URL += "&order=" + this.order;
            post_URL += "&order_key=" + this.order_key;

            this.$http.post(post_URL, {search: this.search}).then(response => {
                const res = response.data;
                this.users_data = res['data'];
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
            this.getUsers();
        },
        modifyItem(index) {
            this.singleModal = true;
            this.modal_type = "modify";
            this.modal_title = "修改登陆用户";
            this.singleItem = Object.assign({}, this.users_data[index]);
        },
        changePage(page) {
            this.page = page;
            this.getUsers();
        },
        changePageSize(page_size) {
            this.page_size = page_size;
            this.getUsers();
        },
        sortChange(value){
            this.order = value.order;
            this.order_key = value.key;
            this.getUsers();
        },
        visibleChange(status) {
            this.singleModal = status;
        },
        closeModal(text) {
            this.singleModal = false;
            this.getUsers();
        },
        removeItem(index) {
            this.$Modal.confirm({
                title: '是否确认删除',
                content: '',
                onOk: () => {
                    var post_URL = baseAPIUrl + "setting/user/" + this.users_data[index].item_number;

                    this.$http.delete(post_URL).then(response => {
                        const res = response.data;
                        if(res['status'] != "success")
                            this.$Message.error(res['message']);

                        this.$Message.success('删除成功!');
                        this.getUsers();
                    }, response => {
                        if(response.status == 401){
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
        addItem() {
            this.modal_type = "add";
            this.modal_title = "增加登陆用户";
            this.singleItem = {};
            this.singleModal = true;
        }
    }
}
</script>
