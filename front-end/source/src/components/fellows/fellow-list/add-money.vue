<template>
    <Row>
        <Form ref="singleItem" :model="singleItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="单号" prop="item" style="display: none;">
                <Input disabled v-model="singleItem.item_number"></Input>
            </FormItem>
            <FormItem label="会员" prop="fellow">
                <Row>
                    <Col span="16">
                        <Select v-model="singleItem.fellow" style="width: 180px;" filterable>
                            <Option v-for="(option, index) in fellow_list" :value="option.value" :key="index" >{{option.label}}</Option>
                        </Select>
                    </Col>
                    <Col span="8">    
                        <Button type="primary" size="small" @click="showFellowInfo">查看会员信息</Button>
                    </Col>
                </Row>                
            </FormItem>
            <FormItem label="卡类型" prop="card_type">
                <Select v-model="singleItem.card_type" placeholder="请选择会员卡类型">
                    <Option v-for="(option, index) in card_type_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem label="充值金额" prop="money">
                <InputNumber style="width: 180px;" v-model="singleItem.money" placeholder="请输入金额"></InputNumber>
            </FormItem>
            <FormItem label="操作员" prop="created_by">
                <Select v-model="singleItem.created_by" placeholder="请选择操作员">
                    <Option v-for="(option, index) in employee_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmit('singleItem')">提交</Button>
                <Button @click="handleReset('singleItem')" style="margin-left: 8px">重置</Button>
            </FormItem>
        </Form>
    </Row>
</template>
<script>
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "AddFellowMoneyItem",
    props: {
        modal_type: '',
        card_type_list: '',
        employee_list: '',
        fellow_list: '',
        employee_list: '',
        card_type_list: '',
        singleItem: {
            fellow: '',
            card_type: '',
            money: 0,
            created_by: '',
            item_number: ''
        }
    },
    data() {
        return {
            ruleValidate: {
                fellow: [
                    { required: true, message: '请选择会员手机号'},
                ],
                card_type: [
                    { required: true, message: '请选择卡类型' }
                ],
                money: [
                    { required: true, message: '请填写金额' },
                    { type: 'number', message: '错误金额'}
                ],
                created_by: [
                    { required: true, message: '请选择开卡人' }
                ]
            }
        }
    },
    methods: {
        showFellowInfo () {
            const fellow_info = this.fellow_list.filter(item => item['value'] == this.singleItem.fellow);
            const content = 
                '<p>姓名：' + fellow_info[0]['name'] + '</p>' +
                '<p>卡类型：' + fellow_info[0]['card_type'] + '</p>' +
                '<p>余额：' + fellow_info[0]['money'] + '</p>' + 
                '<p>手机号：' + fellow_info[0]['value'] + '</p>';
            this.$Modal.success({
                title: "会员信息",
                content: content
            });
        },
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    // var post_URL = baseAPIUrl + "fellow/add_money";

                    // var temp = Object.assign({}, this.singleItem);
                    // temp.birthday = temp.birthday.toString();
                    // this.$http.post(post_URL, temp).then(response => {
                    //     const res = response.data;
                    //     if(res['status'] != "success")
                    //         this.$Message.error(res['message']);
                    //     else{
                    //         this.$Message.success('新增成功!');
                    //         this.$emit('closeModal', 'submit');  
                    //         this.$refs[name].resetFields();    
                    //     }
                    // }, response => {
                    //     if(response.status == 401){
                    //       // this.$Message.error('请登陆');
                    //       this.$router.push({
                    //         name: "login"
                    //       });
                    //     }
                    // });
                } else {
                    this.$Message.error('请查看是否填写完必须输入的项!');
                }
            })
        },
        handleReset (name) {
            this.$refs[name].resetFields();
        }
    }
}
</script>