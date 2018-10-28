<template>
    <div>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="8">
                <Input search enter-button placeholder="请输入关键字搜索" style="width: 300px;float: right;" @on-search="handleSearch" v-model="search"/>
            </Col>
        </Row>
        <Row type="flex" justify="start" class="code-row-bg" style="padding: 10px;">
            <Col span="24">
                <Table border :columns="columns" :data="sell_items_data"></Table>
            </Col>
        </Row>
        <Row type="flex" justify="end" class="code-row-bg">
            <Col span="24">
                <Page :total="entire_data.length" show-total show-sizer :page-size="page_size" :page-size-opts=[2,20,50,100,500] @on-change="changePage" @on-page-size-change="changePageSize" style="float: right;"/>
            </Col>
        </Row>
    </div>
</template>
<script>
const baseAPIUrl = process.env.baseAPIUrl;
    export default {
        name: "SellItems",
        data () {
            return {
                search: '',
                page: 1,
                page_size: 20,
                entire_data: [
                    {
                        raw_id: 1,
                        name: 'John Brown',
                        age: 18,
                        address: 'New York No. 1 Lake Park'
                    },
                    {
                        raw_id: 2,
                        name: 'Jim Green',
                        age: 24,
                        address: 'London No. 1 Lake Park'
                    },
                    {
                        raw_id: 3,
                        name: 'Joe Black',
                        age: 30,
                        address: 'Sydney No. 1 Lake Park'
                    },
                    {
                        raw_id: 4,
                        name: 'Jon Snow',
                        age: 26,
                        address: 'Ottawa No. 2 Lake Park'
                    }
                ],
                columns: [
                    {
                        title: 'Name',
                        key: 'name',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.name)
                            ]);
                        }
                    },
                    {
                        title: 'Age',
                        key: 'age',
                        sortable: true
                    },
                    {
                        title: 'Address',
                        key: 'address',
                        filterRemote(){
                            console.log(this);
                        }
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
                                            this.show(params.index)
                                        }
                                    }
                                }, 'View'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.remove(params.index)
                                        }
                                    }
                                }, 'Delete')
                            ]);
                        }
                    }
                ]
            }
        },
        computed: {
            sell_items_data() {
                return this.entire_data.filter(item => {
                    return item.name.indexOf(this.search.toLowerCase()) > -1
                })
            }
        },
        created: function() {
            this.getSellItems();
        },
        methods: {
            getSellItems() {
                // this.$http.get(baseAPIUrl + "sell_items").then(response => {
                //     this.entire_data = response.data;
                // }, response => {
                //     if(response.status == 401){
                //       this.$Message.error('请登陆');
                //       this.$router.push({
                //         name: "login"
                //       });
                //     }
                // });
            },
            handleSearch(value) {
                
                // this.sell_items_data = this.entire_data.filter(item => item.indexOf(value) > -1)
            },
            show (index) {
                this.$Modal.info({
                    title: 'User Info',
                    content: `Name：${this.sell_items_data[index].name}<br>Age：${this.sell_items_data[index].age}<br>Address：${this.sell_items_data[index].address}`
                })
            },
            remove (index) {
                this.sell_items_data.splice(index, 1);
            },
            changePage(page) {
                this.page = page;
                this.getSellItems();
            },
            changePageSize(page_size) {
                this.page_size = page_size;
                this.getSellItems();
            }
        }
    }
</script>
