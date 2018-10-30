<style lang="less" scoped>
@import 'index.less';
</style>
<template>
    <div>
        <Layout>
            <Header :style="{
                    position: 'fixed',
                    width: '100%',
                    display:'flex',
                    padding: '0',
                    height: '60px',
                    flexDirection:'column',
                    zIndex:20
                }" class="layout-header-bar">
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    position: relative;
                    height:60px;
                    line-height: 60px;
                    z-index: 1;
                    box-shadow: 0 2px 1px 1px rgba(100, 100, 100, 0.1);">
                    <div style="display:flex;align-items:center;padding-left: 100px;">
                        <!-- <img :src="logo" width="100" style="background-color: '#000fff'" /> -->
                        <span style="font-size:18px;font-weight:bold">日常功能区</span>
                        <span style="font-size:14px;padding-left: 20px;">欢迎光临！ {{current_user}}</span>
                    </div>
                    <div style="margin-right:20px">
                        <Button type="text" icon="ios-apps" size="large" @click="enter_admin">进入管理页面</Button>
                        <Button type="text" icon="ios-exit" size="large" @click="quit">退出系统</Button>
                    </div>
                </div> 
                                 
            </Header>
            <Content :style="{
                height: 'calc(100% - 60px)',
                position: 'absolute',
                top: '60px',
                overflow: 'auto',
                padding: '10px',
                width: '100%',
                }" class="index_background">
                <Row :gutter="120" class="row_box">
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center" @click="addSellItem">
                                <img :src="box_img">
                                <h3>开单</h3>
                            </div>
                        </Card>
                    </Col>
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center">
                                <img :src="box_img">
                                <h3>充值</h3>
                            </div>
                        </Card>
                    </Col>
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center">
                                <img :src="box_img">
                                <h3>开卡</h3>
                            </div>
                        </Card>
                    </Col>
                </Row>
                <Row :gutter="120" class="row_box">
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center">
                                <img :src="box_img">
                                <h3>产品消费</h3>
                            </div>
                        </Card>
                    </Col>
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center">
                                <img :src="box_img">
                                <h3>其他</h3>
                            </div>
                        </Card>
                    </Col>
                </Row>
            </Content>
        </Layout>
        <Modal
            v-model="sellItemModal" footer-hide
            title="开单">
            <SellItem :singleItem="sellItem" :modal_type="modal_type" @closeModal="closeSellItemModal" :hairdresser_list="hairdresser_list" :assistant_list="assistant_list" :fellow_list="fellow_list"></SellItem>
        </Modal>
    </div>
</template>
<script>
import SellItem from '@/components/sell-items/sell-item.vue'

import w_box_img from '@/assets/images/barber-razor-scissor.png'
import w_logo from '@/assets/images/logo.png'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "Index",
    components: {
        SellItem
    },
    data() {
        return{
            logo: '',
            box_img: '',
            current_user: '',
            sellItemModal: false,
            modal_type: 'add',
            hairdresser_list: [],
            assistant_list: [],
            fellow_list: [],
            sellItem: {
                hairdresser: '',
                assistant: '',
                item_type: [],
                money: '',
                pay_type: '',
                fellow: '',
                comment: '',
                item_number: ''
            }
        }
    },
    created: function() {
        this.box_img = w_box_img;
        this.logo = w_logo;
        this.getEmployees();
        this.getFellows();
        this.$http.get(baseAPIUrl + "api/user").then(response => {
            this.current_user = response.data["name"];
        }, response => {
          this.$router.push({
            name: "login"
          });
        });
    },
    methods: {
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
        quit(){
            this.$http.get(baseAPIUrl + "logout").then(response => {
              this.$Message.success('退出成功！' + response.data.message);
              this.$router.push({
                name: "login"
              });
            }, response => {
              // this.$Message.error('请登陆');
            });
        },
        enter_admin(){
            this.$router.push({
                name: "dashboard"
              });
        },
        addSellItem(){
            this.sellItemModal = true;
        },
        closeSellItemModal(){
            this.sellItemModal = false;
        }
    }
}
</script>