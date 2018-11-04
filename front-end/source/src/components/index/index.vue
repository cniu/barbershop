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
                            <div style="text-align:center" @click="addFellowMoneyItem">
                                <img :src="box_img">
                                <h3>充值</h3>
                            </div>
                        </Card>
                    </Col>
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center" @click="addFellowItem">
                                <img :src="box_img">
                                <h3>开卡</h3>
                            </div>
                        </Card>
                    </Col>
                </Row>
                <Row :gutter="120" class="row_box">
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center" @click="addProductSellItem">
                                <img :src="box_img">
                                <h3>产品消费</h3>
                            </div>
                        </Card>
                    </Col>
                    <Col span="8">  
                        <Card>
                            <div style="text-align:center" @click="addOtherSellItem">
                                <img :src="box_img">
                                <h3>其他消费</h3>
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
        <Modal
            v-model="fellowItemModal" footer-hide
            title="开卡">
            <FellowItem :singleItem="fellowItem" :modal_type="modal_type" @closeModal="closeFellowItemModal" :card_type_list="card_type_list" :employee_list="employee_list"></FellowItem>
        </Modal>
        <Modal
            v-model="increaseFellowItemModal" footer-hide
            title="充值">
            <IncreaseFellowMoneyItem :singleItem="increaseFellowMoneyItem" :modal_type="modal_type" @closeModal="closeAddFellowMoneyItemModal" :card_type_list="card_type_list" :employee_list="employee_list" :fellow_list="fellow_list"></IncreaseFellowMoneyItem>
        </Modal>
        <Modal
            v-model="productSellItemModal" footer-hide
            title="产品消费">
            <ProductSellItem :singleItem="productSellItem" :modal_type="modal_type" @closeModal="closeProductSellItemModal" :employee_list="employee_list" :fellow_list="fellow_list"></ProductSellItem>
        </Modal>
        <Modal
            v-model="otherSellItemModal" footer-hide
            title="其他消费">
            <OtherSellItem :singleItem="otherSellItem" :modal_type="modal_type" @closeModal="closeOtherSellItemModal" :employee_list="employee_list" :fellow_list="fellow_list"></OtherSellItem>
        </Modal>
    </div>
</template>
<script>
import SellItem from '@/components/sell-items/sell-item.vue'
import FellowItem from '@/components/fellows/fellow-list/sell-item.vue'
import IncreaseFellowMoneyItem from '@/components/fellows/fellow-list/add-money.vue'
import ProductSellItem from '@/components/product-sell/sell-item.vue'
import OtherSellItem from '@/components/other-sell/sell-item.vue'

import w_box_img from '@/assets/images/barber-razor-scissor.png'
import w_logo from '@/assets/images/logo.png'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "Index",
    components: {
        SellItem,
        FellowItem,
        IncreaseFellowMoneyItem,
        ProductSellItem,
        OtherSellItem
    },
    data() {
        return{
            logo: '',
            box_img: '',
            current_user: '',
            sellItemModal: false,
            fellowItemModal: false,
            increaseFellowItemModal: false,
            productSellItemModal: false,
            otherSellItemModal: false,
            modal_type: 'add',
            hairdresser_list: [],
            assistant_list: [],
            fellow_list: [],
            card_type_list: [],
            employee_list: [],
            sellItem: {
                hairdresser: '',
                assistant: '',
                item_type: [],
                money: 0,
                pay_type: '',
                fellow: '',
                comment: '',
                item_number: ''
            },
            fellowItem: {
                name: '',
                phone_number: 0,
                birthday: '',
                card_type: '',
                money: 0,
                created_by: '',
                password: '',
                item_number: ''
            },
            increaseFellowMoneyItem: {
                fellow: '',
                card_type: '',
                money: 0,
                created_by: '',
                item_number: ''
            },
            productSellItem: {
                fellow: '',
                pay_type: '',
                money: 0,
                created_by: '',
                comment: '',
                item_number: ''
            },
            otherSellItem: {
                fellow: '',
                pay_type: '',
                money: 0,
                created_by: '',
                item_number: '',
                comment: ''
            }
        }
    },
    created: function() {
        this.box_img = w_box_img;
        this.logo = w_logo;
        this.getEmployees();
        this.getFellows();
        this.getCardTypeList();
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
                this.employee_list = res['employee_list'];
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
        getCardTypeList() {
            var post_URL = baseAPIUrl + "summarized_setting";

            this.$http.get(post_URL).then(response => {
                const res = response.data;
                this.card_type_list = res['card_type_list'];
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
            this.sellItem = {};
            this.sellItem.birthday = "";
            this.sellItemModal = true;
        },
        closeSellItemModal(){
            this.sellItemModal = false;
        },
        addFellowItem(){
            this.fellowItem = {};
            this.fellowItemModal = true;
        },
        closeFellowItemModal(){
            this.fellowItemModal = false;
        },
        addFellowMoneyItem(){
            this.increaseFellowMoneyItem = {};
            this.increaseFellowItemModal = true;
        },
        closeAddFellowMoneyItemModal(){
            this.increaseFellowItemModal = false;
        },
        addProductSellItem(){
            this.productSellItem = {};
            this.productSellItemModal = true;
        },
        closeProductSellItemModal(){
            this.productSellItemModal = false;
        },
        addOtherSellItem(){
            this.otherSellItem = {};
            this.otherSellItemModal = true;
        },
        closeOtherSellItemModal(){
            this.otherSellItemModal = false;
        },
    }
}
</script>