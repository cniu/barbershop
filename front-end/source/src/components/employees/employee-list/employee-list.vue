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
                <Table border :columns="columns" :data="employee_list_data" @on-sort-change="sortChange"></Table>
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
            <EmployeeItem :singleItem="singleItem" :modal_type="modal_type" @closeModal="closeModal" :employee_type_list="employee_type_list"></EmployeeItem>
        </Modal>
    </div>
</template>
<script>
import EmployeeItem from './sell-item.vue'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "EmployeeList",
    components: {
        EmployeeItem
    },
    data () {
        return {
            employee_type_list: [],
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
            employee_list_data: [],
            columns: [
                {
                    title: '编号',
                    key: 'raw_id',
                    width: 80
                },
                {
                    title: '姓名',
                    key: 'name',
                    sortable: 'custom'
                },
                {
                    title: '手机号',
                    key: 'phone_number',
                    sortable: 'custom'
                },
                {
                    title: '入职日期',
                    key: 'first_day',
                    sortable: 'custom',
                    render: (h, params) => {
                        if(params.row.first_day != "")
                            return h('div', 
                                new Date(params.row.first_day).toLocaleDateString()
                            );
                    }
                },
                {
                    title: '员工类型',
                    key: 'employee_type',
                    sortable: 'custom'
                },
                {
                    title: '底薪',
                    key: 'base_salary',
                    sortable: 'custom'
                },
                {
                    title: '提成比率',
                    key: 'percentage',
                    sortable: 'custom'
                },
                {
                    title: '状态',
                    key: 'status',
                    sortable: 'custom'
                },
                // {
                //     title: '备注',
                //     key: 'comment',
                //     ellipsis: true,
                //     sortable: 'custom'
                // },
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
        this.getEmployeeLists();
        this.getEmployeeTypeList();
    },
    methods: {
        getEmployeeLists() {
            var post_URL = baseAPIUrl + "employees?";
            post_URL += "page=" + this.page;
            post_URL += "&page_size=" + this.page_size;
            post_URL += "&order=" + this.order;
            post_URL += "&order_key=" + this.order_key;

            this.$http.post(post_URL, {search: this.search}).then(response => {
                const res = response.data;
                this.employee_list_data = res['data'];
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
        getEmployeeTypeList() {
            var post_URL = baseAPIUrl + "summarized_setting";

            this.$http.get(post_URL).then(response => {
                const res = response.data;
                this.employee_type_list = res['employee_type_list'];
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
            this.getEmployeeLists();
        },
        modifyItem(index) {
            this.singleModal = true;
            this.modal_type = "modify";
            this.modal_title = "修改员工信息";
            this.singleItem = Object.assign({}, this.employee_list_data[index]);
            if(this.singleItem.first_day != "")
                this.singleItem.first_day = new Date(this.singleItem.first_day);
        },
        changePage(page) {
            this.page = page;
            this.getEmployeeLists();
        },
        changePageSize(page_size) {
            this.page_size = page_size;
            this.getEmployeeLists();
        },
        sortChange(value){
            this.order = value.order;
            this.order_key = value.key;
            this.getEmployeeLists();
        },
        visibleChange(status) {
            this.singleModal = status;
        },
        closeModal(text) {
            this.singleModal = false;
            this.getEmployeeLists();
        },
        removeItem(index) {
            this.$Modal.confirm({
                title: '是否确认删除',
                content: '',
                onOk: () => {
                    var post_URL = baseAPIUrl + "employee/" + this.employee_list_data[index].phone_number;

                    this.$http.delete(post_URL).then(response => {
                        const res = response.data;
                        if(res['status'] != "success")
                            this.$Message.error(res['message']);
                        else{
                            this.$Message.success('删除成功!');
                            this.getEmployeeLists();
                        }
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
            this.modal_title = "新增员工";
            this.singleItem = {};
            this.singleItem.first_day = "";
            this.singleModal = true;
        }
    }
}
</script>
